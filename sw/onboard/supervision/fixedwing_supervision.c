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

/* scale signed 32bit to unsigned 8bit value for servo and apply trim */
static inline uint8_t
trim_and_scale(int32_t command, int32_t trim, int8_t scale)
{
    uint32_t c = command + INT32_MAX;
    return ((c + trim) / scale) / (UINT32_MAX / UINT8_MAX);
}

void supervision_run(int32_t out[], int32_t in[], bool_t _motors_on)
{
    out[SERVO_THROTTLE] = trim_and_scale(in[COMMAND_THRUST], 0, 1);
    out[SERVO_ELEVATOR] = trim_and_scale(in[COMMAND_PITCH], 0, 1);
    out[SERVO_AILERON] = trim_and_scale(in[COMMAND_ROLL], 0, 1);
    out[SERVO_RUDDER] = trim_and_scale(in[COMMAND_YAW], 0, 1);
}

