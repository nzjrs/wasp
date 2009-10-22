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
#ifndef SUPERVISION_H
#define SUPERVISION_H

#include "std.h"

/** 
 * Run the actuator model.
 * 
 * Converts the calculated outputs from the autopilot into the range
 * for the actuators, applying any scaling or trimming.
 *
 * @param motor_commands Array of NUM_MOTORS commands in range 
 * MIN_PPRZ -> MAX_PPRZ
 * @param autopilot_commands An array of NUM_COMMANDS in range
 * INT32_MIN -> INT32_MAX
 * @param motors_on TRUE if the motors/actuators should be 'on', whatever
 * on means for the specific actuator
 */
void
supervision_run(pprz_t motor_commands[], int32_t autopilot_commands[], bool_t motors_on);

#endif /* SUPERVISION_H */
