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

#include "stabilization.h"
#include "fixedwing_stabilization.h"

void fixedwing_stabiliziation_h_run(void)
{
    ;
}

void fixedwing_stabiliziation_v_run(void)
{
    ;
}

void stabilization_init(void)
{
    pid_init(&pid_pitch, PID_PITCH_P, PID_PITCH_I, PID_PITCH_D);
    pid_init(&pid_roll, PID_ROLL_P, PID_ROLL_I, PID_ROLL_D);
    pid_init(&pid_yaw, PID_YAW_P, PID_YAW_I, PID_YAW_D);
}

