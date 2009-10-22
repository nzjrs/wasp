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
#include "rc.h"
#include "autopilot.h"
#include "actuators.h"
#include "supervision.h"

#include "generated/settings.h"
#include "generated/radio.h"

uint8_t     autopilot_mode;
bool_t      autopilot_motors_on;
bool_t      autopilot_in_flight;
uint32_t    autopilot_motors_on_counter;
uint32_t    autopilot_in_flight_counter;

int32_t autopilot_commands[COMMAND_NB];
int32_t autopilot_commands_failsafe[COMMAND_NB] = COMMAND_FAILSAFE;

/* Autopilot modes: RATE_DIRECT is manual control, ATTITUDE_DIRECT is 
stabilized flight, i.e. heading hold */

void autopilot_init(void)
{
    autopilot_mode = BOOZ2_AP_MODE_FAILSAFE;
    autopilot_motors_on = FALSE;
    autopilot_in_flight = FALSE;
    autopilot_motors_on_counter = 0;
    autopilot_in_flight_counter = 0;
}

void autopilot_periodic(void)
{
    if ( autopilot_mode == BOOZ2_AP_MODE_FAILSAFE ||
         autopilot_mode == BOOZ2_AP_MODE_KILL ) 
    {
        uint8_t i;

        for (i = 0; i < COMMAND_NB; i++)
            autopilot_commands[i] = 0;
    }
    else
    {
        //fixedwing_guidance_h_run( autopilot_commands[]);        
    }
}

void autopilot_on_rc_event(void)
{

  /* I think this should be hidden in rc code */
  /* the ap gets a mode everytime - the rc filters it */
  if (rc_values_contains_avg_channels) {
    uint8_t new_autopilot_mode = autopilot_mode_of_radio(rc_values[RADIO_MODE]);
    autopilot_set_mode(new_autopilot_mode);
    rc_values_contains_avg_channels = FALSE;
  }

}

void autopilot_set_mode(uint8_t new_autopilot_mode)
{
    if (new_autopilot_mode != autopilot_mode) 
    {
        bool_t ok = TRUE;
        switch (new_autopilot_mode)
        {
            case BOOZ2_AP_MODE_FAILSAFE:
            case BOOZ2_AP_MODE_KILL:
                break;
            case BOOZ2_AP_MODE_RATE_DIRECT:
                break;
            case BOOZ2_AP_MODE_ATTITUDE_DIRECT:
                /* record current heading */
                break;
            default:
                ok = FALSE;
                break;
        }
        if (ok)
            autopilot_mode = new_autopilot_mode;
    }
}

void autopilot_set_actuators(void)
{
    int32_t motor_commands[MOTOR_NB];

    supervision_run(motor_commands, autopilot_commands, autopilot_motors_on);


    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}
