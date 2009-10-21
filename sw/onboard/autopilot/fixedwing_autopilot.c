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

#include "actuators.h"

#include "generated/settings.h"

uint8_t     autopilot_mode;
bool_t      autopilot_motors_on;
bool_t      autopilot_in_flight;
uint32_t    autopilot_motors_on_counter;
uint32_t    autopilot_in_flight_counter;

void autopilot_init(void)
{

}

void autopilot_periodic(void)
{

}

void autopilot_on_rc_event(void)
{

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
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}
