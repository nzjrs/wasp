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
#ifndef AUTOPILOT_H
#define AUTOPILOT_H

#include "std.h"
#include "generated/settings.h"

/* Need to rename them both to actuators */
#if SERVO_NB != MOTOR_NB
#error NOT IMPLEMETED YET
#endif

typedef enum {
    AP_MODE_FAILSAFE = 0,
    AP_MODE_KILL,
    AP_MODE_RATE_DIRECT,
    AP_MODE_ATTITUDE_DIRECT,
    AP_MODE_RATE_RC_CLIMB,
    AP_MODE_ATTITUDE_RC_CLIMB,
    AP_MODE_ATTITUDE_CLIMB,
    AP_MODE_ATTITUDE_HOLD,
    AP_MODE_HOVER_DIRECT,
    AP_MODE_HOVER_CLIMB,
    AP_MODE_NAV,
    AP_MODE_RC_DIRECT
} AutopilotMode_t;

typedef struct __Autopilot {
    AutopilotMode_t mode;
    AutopilotMode_t mode_auto2;
    bool_t          motors_on;
    bool_t          in_flight;
    int32_t         commands[COMMAND_NB];
    int32_t         motor_commands[MOTOR_NB];
} Autopilot_t;

AutopilotMode_t
autopilot_mode_of_radio(pprz_t mode_channel);

/* Implementations must provide these */
extern uint32_t     autopilot_motors_on_counter;
extern uint32_t     autopilot_in_flight_counter;
extern Autopilot_t  autopilot;

void
autopilot_init(void);

void
autopilot_periodic(void);

void
autopilot_on_rc_event(void);

void
autopilot_set_mode(AutopilotMode_t new_autopilot_mode);

void
autopilot_set_actuators(void);

void
autopilot_set_motors(bool_t on);

void
autopilot_kill(void);

#endif /* AUTOPILOT_H */
