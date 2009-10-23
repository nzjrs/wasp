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

typedef struct __BoozSupervision {
    int32_t trim[SUPERVISION_NB_MOTOR];
    uint32_t nb_failure;
} BoozSupervision_t;

static BoozSupervision_t supervision;

static const int32_t roll_coef[SUPERVISION_NB_MOTOR]   = SUPERVISION_ROLL_COEF;
static const int32_t pitch_coef[SUPERVISION_NB_MOTOR]  = SUPERVISION_PITCH_COEF;
static const int32_t yaw_coef[SUPERVISION_NB_MOTOR]    = SUPERVISION_YAW_COEF;
static const int32_t thrust_coef[SUPERVISION_NB_MOTOR] = SUPERVISION_THRUST_COEF;

void supervision_init(void) {
    uint8_t i;
    for (i=0; i<SUPERVISION_NB_MOTOR; i++) {
        supervision.trim[i] =
            roll_coef[i]  * SUPERVISION_TRIM_A +
            pitch_coef[i] * SUPERVISION_TRIM_E +
            yaw_coef[i]   * SUPERVISION_TRIM_R;
    }
    supervision.nb_failure = 0;
}

static inline void offset_commands(int32_t commands[], int32_t offset) {
    uint8_t j;
    for (j=0; j<SUPERVISION_NB_MOTOR; j++)
        commands[j] += (offset);
}

static inline void bound_commands(int32_t commands[]) {
    uint8_t j;
    for (j=0; j<SUPERVISION_NB_MOTOR; j++)
        Bound(commands[j], SUPERVISION_MIN_MOTOR, SUPERVISION_MAX_MOTOR);
}

void supervision_run(int32_t out_cmd[], int32_t in_cmd[], bool_t motors_on)
{
    uint8_t i;
    if (motors_on) {
        int32_t min_cmd = INT32_MAX;
        int32_t max_cmd = INT32_MIN;
        for (i=0; i<SUPERVISION_NB_MOTOR; i++) {
            out_cmd[i] =
                (thrust_coef[i] * in_cmd[COMMAND_THRUST] +
                 roll_coef[i]   * in_cmd[COMMAND_ROLL]   +
                 pitch_coef[i]  * in_cmd[COMMAND_PITCH]  +
                 yaw_coef[i]    * in_cmd[COMMAND_YAW]    +
                 supervision.trim[i]) / SUPERVISION_SCALE;
            if (out_cmd[i] < min_cmd)
                min_cmd = out_cmd[i];
            if (out_cmd[i] > max_cmd)
                max_cmd = out_cmd[i];
        }
        if (min_cmd < SUPERVISION_MIN_MOTOR && max_cmd > SUPERVISION_MAX_MOTOR)
            supervision.nb_failure++;
        if (min_cmd < SUPERVISION_MIN_MOTOR)
            offset_commands(out_cmd, -(min_cmd - SUPERVISION_MIN_MOTOR));
        if (max_cmd > SUPERVISION_MAX_MOTOR)
            offset_commands(out_cmd, -(max_cmd - SUPERVISION_MAX_MOTOR));
            bound_commands(out_cmd);
    } else {
        for (i=0; i<SUPERVISION_NB_MOTOR; i++)
            out_cmd[i] = 0;
    }
}

