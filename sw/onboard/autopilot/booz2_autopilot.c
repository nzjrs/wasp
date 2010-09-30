/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */

#include "autopilot.h"

#include "rc.h"
#include "actuators.h"
#include "supervision.h"
#include "control/quad/booz2_guidance.h"

Autopilot_t autopilot;
uint32_t    autopilot_motors_on_counter;
uint32_t    autopilot_in_flight_counter;
int32_t     booz2_commands_failsafe[COMMAND_NB] = COMMAND_FAILSAFE;

#define BOOZ2_AUTOPILOT_MOTOR_ON_TIME     40
#define BOOZ2_AUTOPILOT_IN_FLIGHT_TIME    40
#define BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD (MAX_PPRZ / 20)
#define BOOZ2_AUTOPILOT_YAW_TRESHOLD      (MAX_PPRZ * 19 / 20)

void autopilot_init(void) {
    autopilot.mode = AP_MODE_FAILSAFE;
    autopilot.motors_on = FALSE;
    autopilot.in_flight = FALSE;
    autopilot.mode_auto2 = AUTOPILOT_MODE_AUTO2;

    autopilot_motors_on_counter = 0;
    autopilot_in_flight_counter = 0;

    booz2_guidance_init();
}

static inline void autopilot_set_commands( int32_t *in_cmd, uint8_t in_flight, uint8_t motors_on )
{
    autopilot.commands[COMMAND_PITCH]  = in_cmd[COMMAND_PITCH];
    autopilot.commands[COMMAND_ROLL]   = in_cmd[COMMAND_ROLL];
    autopilot.commands[COMMAND_YAW]    = (in_flight) ? in_cmd[COMMAND_YAW] : 0;
    autopilot.commands[COMMAND_THRUST] = (motors_on) ? in_cmd[COMMAND_THRUST] : 0;
}

void autopilot_periodic(void) 
{
  
    if ( !autopilot.motors_on ||
         autopilot.mode == AP_MODE_FAILSAFE ||
         autopilot.mode == AP_MODE_KILL ) 
    {
        autopilot_set_commands(
            booz2_commands_failsafe, 
            autopilot.in_flight,
            autopilot.motors_on);
    }
    else
    {
        booz2_guidance_run( autopilot.in_flight );
        autopilot_set_commands(
            booz2_stabilization_cmd, 
            autopilot.in_flight,
            autopilot.motors_on);
    }

}

void autopilot_set_actuators(void)
{
#ifdef KILL_MOTORS
    uint8_t i;
    for (i = 0; i < MOTOR_NB; i++)
        autopilot.motor_commands = 0;
#else
    supervision_run(autopilot.motor_commands, autopilot.commands, autopilot.motors_on);
#endif
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_FRONT, autopilot.motor_commands[MOTOR_FRONT]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_BACK, autopilot.motor_commands[MOTOR_BACK]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_RIGHT, autopilot.motor_commands[MOTOR_RIGHT]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_LEFT, autopilot.motor_commands[MOTOR_LEFT]);
    actuators_commit(ACTUATOR_BANK_MOTORS);
}

void autopilot_set_mode(AutopilotMode_t new_autopilot_mode) 
{
    bool_t ok = TRUE;
    uint8_t h_mode = BOOZ2_GUIDANCE_H_MODE_KILL;
    uint8_t v_mode = BOOZ2_GUIDANCE_V_MODE_KILL;

    if (new_autopilot_mode != autopilot.mode || new_autopilot_mode == AP_MODE_KILL) {
        /* horizontal mode */
        switch (new_autopilot_mode) {
            case AP_MODE_FAILSAFE:
            case AP_MODE_KILL:
                autopilot.motors_on = FALSE;
                h_mode = BOOZ2_GUIDANCE_H_MODE_KILL;
                break;
            case AP_MODE_RC_DIRECT:
                h_mode = BOOZ2_GUIDANCE_H_MODE_RATE;
                break;
            case AP_MODE_ATTITUDE_DIRECT:
                h_mode = BOOZ2_GUIDANCE_H_MODE_ATTITUDE;
                break;
            case AP_MODE_HOVER_DIRECT:
                h_mode = BOOZ2_GUIDANCE_H_MODE_HOVER;
                break;
            default:
                ok = FALSE;
                break;
        }
        /* vertical mode */
        switch (new_autopilot_mode) {
            case AP_MODE_FAILSAFE:
            case AP_MODE_KILL:
                v_mode = BOOZ2_GUIDANCE_V_MODE_KILL;
                break;
            case AP_MODE_RC_DIRECT:
            case AP_MODE_ATTITUDE_DIRECT:
            case AP_MODE_HOVER_DIRECT:
                v_mode = BOOZ2_GUIDANCE_V_MODE_RC_DIRECT;
                break;
            default:
                ok = FALSE;
                break;
        }
        if (ok) {
            booz2_guidance_mode_changed(h_mode, v_mode);
            autopilot.mode = new_autopilot_mode;
        }
    } 

}

static inline void autopilot_check_in_flight(void)
{
    if (autopilot.in_flight) 
    {
        if (autopilot_in_flight_counter > 0) 
        {
            if (rc_values[RADIO_THROTTLE] < BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD) 
            {
                autopilot_in_flight_counter--;
                if (autopilot_in_flight_counter == 0) 
                {
                    autopilot.in_flight = FALSE;
                }
            }
            else
            {	/* rc throttle > threshold */
                autopilot_in_flight_counter = BOOZ2_AUTOPILOT_IN_FLIGHT_TIME;
            }
        }
    }
    else
    { /* not in flight */
        if (autopilot_in_flight_counter < BOOZ2_AUTOPILOT_IN_FLIGHT_TIME &&
            autopilot.motors_on) 
        {
            if (rc_values[RADIO_THROTTLE] > BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD) 
            {
                autopilot_in_flight_counter++;
                if (autopilot_in_flight_counter == BOOZ2_AUTOPILOT_IN_FLIGHT_TIME)
                    autopilot.in_flight = TRUE;
            }
            else
            { /*  rc throttle < threshold */
                autopilot_in_flight_counter = 0;
            }
        }
    }
}

static inline void autopilot_check_motors_on(void)
{
    if (autopilot.motors_on)
    {
        if (rc_values[RADIO_THROTTLE] < BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD &&
            (rc_values[RADIO_YAW] > BOOZ2_AUTOPILOT_YAW_TRESHOLD ||
             rc_values[RADIO_YAW] < -BOOZ2_AUTOPILOT_YAW_TRESHOLD)) 
        {
            if ( autopilot_motors_on_counter > 0) 
            {
                autopilot_motors_on_counter--;
                if (autopilot_motors_on_counter == 0)
                    autopilot.motors_on = FALSE;
            }
        }
        else
        { /* sticks not in the corner */
            autopilot_motors_on_counter = BOOZ2_AUTOPILOT_MOTOR_ON_TIME;
        }
    }
    else
    { /* motors off */
        if (rc_values[RADIO_THROTTLE] < BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD &&
            (rc_values[RADIO_YAW] > BOOZ2_AUTOPILOT_YAW_TRESHOLD ||
             rc_values[RADIO_YAW] < -BOOZ2_AUTOPILOT_YAW_TRESHOLD))
        {
            if ( autopilot_motors_on_counter <  BOOZ2_AUTOPILOT_MOTOR_ON_TIME) 
            {
                autopilot_motors_on_counter++;
                if (autopilot_motors_on_counter == BOOZ2_AUTOPILOT_MOTOR_ON_TIME)
                    autopilot.motors_on = TRUE;
            }
        }
        else
        {
            autopilot_motors_on_counter = 0;
        }
    }
}

void autopilot_on_rc_event(void) 
{

    /* I think this should be hidden in rc code */
    /* the ap gets a mode everytime - the rc filters it */
    if (rc_values_contains_avg_channels) {
        AutopilotMode_t new_autopilot_mode = autopilot_mode_of_radio(rc_values[RADIO_MODE]);
        autopilot_set_mode(new_autopilot_mode);
        rc_values_contains_avg_channels = FALSE;
    }

    autopilot_check_motors_on();
    autopilot_check_in_flight();

    booz2_guidance_read_rc(autopilot.in_flight);

}

void autopilot_set_motors(bool_t on)
{
    /* only turn the motors on/off while on ground */
    if (!autopilot.in_flight) {
        if (on) {
            autopilot_motors_on_counter = BOOZ2_AUTOPILOT_MOTOR_ON_TIME;
            autopilot.motors_on = TRUE;
        } else {
            autopilot_motors_on_counter = 0;
            autopilot.motors_on = FALSE;
        }
    }
}

void autopilot_get_h_and_v_control_modes(uint8_t *h_mode, uint8_t *v_mode)
{
    *h_mode = booz2_guidance_h_mode;
    *v_mode = booz2_guidance_v_mode;
}

