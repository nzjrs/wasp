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
#include "ahrs.h"
#include "stabilization.h"
#include "fixedwing_stabilization.h"

#include "generated/settings.h"
#include "generated/radio.h"

PID_t   pid_pitch;
PID_t   pid_roll;
PID_t   pid_yaw;

typedef struct _Int32RC {
    int32_t     roll;
    int32_t     pitch;
    int32_t     yaw;
    int32_t     throttle;
} Int32RC_t;

static void fixedwing_alt_read_rc(Int32RC_t *rc)
{
    rc->roll = ((int32_t)rc_values[RADIO_ROLL]) * (INT32_MAX/MAX_PPRZ);
    rc->pitch = ((int32_t)rc_values[RADIO_PITCH]) * (INT32_MAX/MAX_PPRZ);
    rc->yaw = ((int32_t)rc_values[RADIO_YAW]) * (INT32_MAX/MAX_PPRZ);
    rc->throttle = ((int32_t)rc_values[RADIO_THROTTLE]) * (INT32_MAX/MAX_PPRZ);
}

/* Basic fixed wing autopilot

Horizontal mode PID controllers handle roll,heading,rudder
 - Ailerons are controlled by roll estimate from the IMU.
 - Elevators are controlled by the pitch estimate from the IMU
 - Heading is controlled by the rudder

Vertical mode PID controller handles altitude
 - Altitude is controlled using the throttle

Note:
 - Radio values range from -9600 -> 9600
*/

void fixedwing_stabiliziation_alt_h_run(int32_t *commands)
{
    Int32RC_t   rc;

    fixedwing_alt_read_rc(&rc);

    /* Roll */
    commands[COMMAND_ROLL] = pid_calculate_with_sp(
            &pid_roll,
            rc.roll,                        /* sp */
            ahrs.ltp_to_body_euler.theta,   /* val, roll = theta */
            1);                             /* dt */

    /* Pitch */
    commands[COMMAND_PITCH] = pid_calculate_with_sp(
            &pid_pitch,
            rc.pitch,                       /* sp */
            ahrs.ltp_to_body_euler.phi,     /* val, pitch = phi */
            1);                             /* dt */

    /* Heading */
    commands[COMMAND_YAW] = pid_calculate_with_sp(
            &pid_yaw,
            rc.yaw,                         /* sp */
            ahrs.ltp_to_body_euler.psi,     /* val, yaw = psi */
            1);                             /* dt */

}

void fixedwing_stabiliziation_alt_v_run(int32_t *commands)
{
    /* RADIO_THROTTLE is 0 -> 9600 */
    if (rc_values[RADIO_THROTTLE] < 0)
        commands[COMMAND_THRUST] = 0;
    else
        commands[COMMAND_THRUST] = rc_values[RADIO_THROTTLE] * (INT32_MAX/MAX_PPRZ);
}

void stabilization_init(void)
{
    pid_init(&pid_pitch, PID_PITCH_P, PID_PITCH_I, PID_PITCH_D);
    pid_init(&pid_roll, PID_ROLL_P, PID_ROLL_I, PID_ROLL_D);
    pid_init(&pid_yaw, PID_YAW_P, PID_YAW_I, PID_YAW_D);
}

