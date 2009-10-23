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

#include "std.h"
#include "supervision.h"
#include "generated/settings.h"

Supervision_t supervision_trim;

/* scale signed 32bit to unsigned 8bit value (zero at 127)) for servo and apply trim */
static inline uint8_t
trim_and_scale(int32_t command, int32_t trim)
{
    uint32_t c = (uint32_t)command + trim + INT32_MAX;
    return c / (UINT32_MAX / UINT8_MAX);
}

/* scale unsigned 32bit to unsigned 8bit value for throttle and apply trim */
static inline uint8_t
trim_and_scale_throttle(int32_t command, int32_t trim)
{
    uint32_t c = (uint32_t)command + trim;
    return c / (INT32_MAX / UINT8_MAX);
}

void supervision_run(int32_t out[], int32_t in[], bool_t _motors_on)
{
    out[SERVO_THROTTLE] = trim_and_scale_throttle(in[COMMAND_THRUST], supervision_trim.trim_t);
    out[SERVO_ELEVATOR] = trim_and_scale(in[COMMAND_PITCH], supervision_trim.trim_e);
    out[SERVO_AILERON]  = trim_and_scale(in[COMMAND_ROLL], supervision_trim.trim_a);
    out[SERVO_RUDDER]   = trim_and_scale(in[COMMAND_YAW], supervision_trim.trim_r);
}

void supervision_init(void)
{
    supervision_set_trim(SUPERVISION_TRIM_A, SUPERVISION_TRIM_E, SUPERVISION_TRIM_R, SUPERVISION_TRIM_R);
}

void
supervision_set_trim(int32_t trim_a, int32_t trim_e, int32_t trim_r, int32_t trim_t)
{
    supervision_trim.trim_a = trim_a;
    supervision_trim.trim_e = trim_e;
    supervision_trim.trim_r = trim_r;
    supervision_trim.trim_t = trim_t;
}
