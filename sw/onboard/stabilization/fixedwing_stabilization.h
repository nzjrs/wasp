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
#ifndef _FW_STABILIZATION_H_
#define _FW_STABILIZATION_H_

#include "std.h"
#include "math/pid_int.h"

PID_t   pid_pitch;
PID_t   pid_roll;
PID_t   pid_yaw;

void fixedwing_stabiliziation_alt_h_run(int32_t *commands);
void fixedwing_stabiliziation_alt_v_run(int32_t *commands);

#endif /* _FW_STABILIZATION_H_ */
