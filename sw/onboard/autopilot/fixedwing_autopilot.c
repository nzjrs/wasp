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

#include "guidance/fixedwing_guidance.h"

#include "generated/settings.h"
#include "generated/radio.h"

#include "comm.h"
#include "messages.h"
#include "generated/messages.h"

Autopilot_t     autopilot;
int32_t         autopilot_commands_failsafe[COMMAND_NB] = COMMAND_FAILSAFE;
const uint8_t   servo_addr[SERVO_NB] = SERVO_ADDR;

/* Autopilot modes: RATE_DIRECT is manual control, ATTITUDE_DIRECT is 
stabilized flight, i.e. heading hold */

void autopilot_init(void)
{
    uint8_t i;

    autopilot.mode = AP_MODE_FAILSAFE;
    autopilot.motors_on = FALSE;
    autopilot.in_flight = FALSE;
    autopilot.mode_auto2 = AUTOPILOT_MODE_AUTO2;

    /* set outputs to failsafe positions, except for throttle, which
    is always 0 at init */
    for (i = 0; i < COMMAND_NB; i++)
        autopilot.commands[i] = autopilot_commands_failsafe[i];
    autopilot.commands[COMMAND_THRUST] = 0;
}

void autopilot_periodic(void)
{
    uint8_t i;

    switch (autopilot.mode)
    {
        case AP_MODE_FAILSAFE:
        case AP_MODE_KILL:
            for (i = 0; i < COMMAND_NB; i++)
                autopilot.commands[i] = autopilot_commands_failsafe[i];
            break;
        case AP_MODE_RATE_DIRECT:
            /* scale radio values to full range */
            autopilot.commands[COMMAND_PITCH] = rc_values[RADIO_PITCH] * (INT32_MAX/MAX_PPRZ);
            autopilot.commands[COMMAND_ROLL] = rc_values[RADIO_ROLL] * (INT32_MAX/MAX_PPRZ);
            autopilot.commands[COMMAND_YAW] = rc_values[RADIO_YAW] * (INT32_MAX/MAX_PPRZ);

            /* RADIO_THROTTLE is 0 -> 9600 */
            if (rc_values[RADIO_THROTTLE] < 0)
                autopilot.commands[COMMAND_THRUST] = 0;
            else
                autopilot.commands[COMMAND_THRUST] = rc_values[RADIO_THROTTLE] * (INT32_MAX/MAX_PPRZ);
            break;
        case AP_MODE_ATTITUDE_DIRECT:
            break;
        default:
            break;
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

void autopilot_set_mode(AutopilotMode_t new_autopilot_mode)
{
    if (new_autopilot_mode != autopilot.mode) 
    {
        bool_t ok = TRUE;
        switch (new_autopilot_mode)
        {
            case AP_MODE_FAILSAFE:
            case AP_MODE_KILL:
                break;
            case AP_MODE_RATE_DIRECT:
                break;
            case AP_MODE_ATTITUDE_DIRECT:
                break;
            default:
                ok = FALSE;
                break;
        }
        if (ok)
            autopilot.mode = new_autopilot_mode;
    }
}

void autopilot_set_actuators(void)
{
    uint8_t i;

    supervision_run(autopilot.motor_commands, autopilot.commands, autopilot.motors_on);

    for (i = 0; i < SERVO_NB; i++)
        actuators_set(ACTUATOR_BANK_SERVOS | servo_addr[i], autopilot.motor_commands[i]);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}
