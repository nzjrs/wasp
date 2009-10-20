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
#include "booz2_navigation.h"
#include "guidance/booz2_guidance_h.h"
#include "guidance/booz2_guidance_v.h"
#include "stabilization/booz2_stabilization.h"
#include "booz2_supervision.h"

uint8_t autopilot_mode;
bool_t  autopilot_motors_on;
bool_t  autopilot_in_flight;
uint32_t autopilot_motors_on_counter;
uint32_t autopilot_in_flight_counter;

int32_t booz2_commands[COMMAND_NB];
int32_t booz2_commands_failsafe[COMMAND_NB] = COMMAND_FAILSAFE;

#define BOOZ2_AUTOPILOT_MOTOR_ON_TIME     40
#define BOOZ2_AUTOPILOT_IN_FLIGHT_TIME    40
#define BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD (MAX_PPRZ / 20)
#define BOOZ2_AUTOPILOT_YAW_TRESHOLD      (MAX_PPRZ * 19 / 20)

void autopilot_init(void) {
    autopilot_mode = BOOZ2_AP_MODE_FAILSAFE;
    autopilot_motors_on = FALSE;
    autopilot_in_flight = FALSE;
    autopilot_motors_on_counter = 0;
    autopilot_in_flight_counter = 0;
    autopilot_mode_auto2 = AUTOPILOT_MODE_AUTO2;
}

static inline void autopilot_set_commands( int32_t *in_cmd, uint8_t in_flight, uint8_t motors_on )
{
    booz2_commands[COMMAND_PITCH]  = in_cmd[COMMAND_PITCH];
    booz2_commands[COMMAND_ROLL]   = in_cmd[COMMAND_ROLL];
    booz2_commands[COMMAND_YAW]    = (in_flight) ? in_cmd[COMMAND_YAW] : 0;
    booz2_commands[COMMAND_THRUST] = (motors_on) ? in_cmd[COMMAND_THRUST] : 0;
}

void autopilot_periodic(void) {
  
    if ( !autopilot_motors_on ||
         autopilot_mode == BOOZ2_AP_MODE_FAILSAFE ||
         autopilot_mode == BOOZ2_AP_MODE_KILL ) 
    {
        autopilot_set_commands(
            booz2_commands_failsafe, 
            autopilot_in_flight,
            autopilot_motors_on);
    }
    else
    {
        RunOnceEvery(50, nav_periodic_task_10Hz())
        booz2_guidance_v_run( autopilot_in_flight );
        booz2_guidance_h_run( autopilot_in_flight );
        autopilot_set_commands(
            booz2_stabilization_cmd, 
            autopilot_in_flight,
            autopilot_motors_on);
    }

}

void autopilot_set_actuators(void)
{
#ifdef KILL_MOTORS
    pprz_t motor_commands[MOTOR_NB] = {0,0,0,0};
#else
    pprz_t motor_commands[MOTOR_NB];
    BOOZ2_SUPERVISION_RUN(motor_commands, booz2_commands, autopilot_motors_on);
#endif
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_FRONT, motor_commands[MOTOR_FRONT]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_BACK, motor_commands[MOTOR_BACK]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_RIGHT, motor_commands[MOTOR_RIGHT]);
    actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_LEFT, motor_commands[MOTOR_LEFT]);
    actuators_commit(ACTUATOR_BANK_MOTORS);
}

void autopilot_set_mode(uint8_t new_autopilot_mode) {

  if (new_autopilot_mode != autopilot_mode) {
    /* horizontal mode */
    switch (new_autopilot_mode) {
    case BOOZ2_AP_MODE_FAILSAFE:
    case BOOZ2_AP_MODE_KILL:
      autopilot_motors_on = FALSE;
      booz2_guidance_h_mode_changed(BOOZ2_GUIDANCE_H_MODE_KILL);
      break;
    case BOOZ2_AP_MODE_RATE_DIRECT:
    case BOOZ2_AP_MODE_RATE_Z_HOLD:
      booz2_guidance_h_mode_changed(BOOZ2_GUIDANCE_H_MODE_RATE);
      break;
    case BOOZ2_AP_MODE_ATTITUDE_DIRECT:
    case BOOZ2_AP_MODE_ATTITUDE_CLIMB:
    case BOOZ2_AP_MODE_ATTITUDE_Z_HOLD:
      booz2_guidance_h_mode_changed(BOOZ2_GUIDANCE_H_MODE_ATTITUDE);
      break;
    case BOOZ2_AP_MODE_HOVER_DIRECT:
    case BOOZ2_AP_MODE_HOVER_CLIMB:
    case BOOZ2_AP_MODE_HOVER_Z_HOLD:
      booz2_guidance_h_mode_changed(BOOZ2_GUIDANCE_H_MODE_HOVER);
      break;
    case BOOZ2_AP_MODE_NAV:
      booz2_guidance_h_mode_changed(BOOZ2_GUIDANCE_H_MODE_NAV);
      break;
    }
    /* vertical mode */
    switch (new_autopilot_mode) {
    case BOOZ2_AP_MODE_FAILSAFE:
    case BOOZ2_AP_MODE_KILL:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_KILL);
      break;
    case BOOZ2_AP_MODE_RATE_DIRECT:
    case BOOZ2_AP_MODE_ATTITUDE_DIRECT:
    case BOOZ2_AP_MODE_HOVER_DIRECT:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_RC_DIRECT);
      break;
    case BOOZ2_AP_MODE_RATE_RC_CLIMB:
    case BOOZ2_AP_MODE_ATTITUDE_RC_CLIMB:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_RC_CLIMB);
      break;
    case BOOZ2_AP_MODE_ATTITUDE_CLIMB:
    case BOOZ2_AP_MODE_HOVER_CLIMB:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_CLIMB);
      break;
    case BOOZ2_AP_MODE_RATE_Z_HOLD:
    case BOOZ2_AP_MODE_ATTITUDE_Z_HOLD:
    case BOOZ2_AP_MODE_HOVER_Z_HOLD:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_HOVER);
      break;
    case BOOZ2_AP_MODE_NAV:
      booz2_guidance_v_mode_changed(BOOZ2_GUIDANCE_V_MODE_NAV);
      break;
    }
    autopilot_mode = new_autopilot_mode;
  } 
  
}

static inline void autopilot_check_in_flight(void)
{
    if (autopilot_in_flight) 
    {
        if (autopilot_in_flight_counter > 0) 
        {
            if (rc_values[RADIO_THROTTLE] < BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD) 
            {
                autopilot_in_flight_counter--;
                if (autopilot_in_flight_counter == 0) 
                {
                    autopilot_in_flight = FALSE;
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
            autopilot_motors_on) 
        {
            if (rc_values[RADIO_THROTTLE] > BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD) 
            {
                autopilot_in_flight_counter++;
                if (autopilot_in_flight_counter == BOOZ2_AUTOPILOT_IN_FLIGHT_TIME)
                    autopilot_in_flight = TRUE;
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
    if (autopilot_motors_on)
    {
        if (rc_values[RADIO_THROTTLE] < BOOZ2_AUTOPILOT_THROTTLE_TRESHOLD &&
            (rc_values[RADIO_YAW] > BOOZ2_AUTOPILOT_YAW_TRESHOLD ||
             rc_values[RADIO_YAW] < -BOOZ2_AUTOPILOT_YAW_TRESHOLD)) 
        {
            if ( autopilot_motors_on_counter > 0) 
            {
                autopilot_motors_on_counter--;
                if (autopilot_motors_on_counter == 0)
                    autopilot_motors_on = FALSE;
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
                    autopilot_motors_on = TRUE;
            }
        }
        else
        {
            autopilot_motors_on_counter = 0;
        }
    }
}

void autopilot_on_rc_event(void) {

  /* I think this should be hidden in rc code */
  /* the ap gets a mode everytime - the rc filters it */
  if (rc_values_contains_avg_channels) {
    uint8_t new_autopilot_mode = autopilot_mode_of_radio(rc_values[RADIO_MODE]);
    autopilot_set_mode(new_autopilot_mode);
    rc_values_contains_avg_channels = FALSE;
  }

  autopilot_check_motors_on();
  autopilot_check_in_flight();

  booz2_guidance_v_read_rc();
  booz2_guidance_h_read_rc(autopilot_in_flight);

}
