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
#ifndef BOOZ2_STABILIZATION_H
#define BOOZ2_STABILIZATION_H

#include "std.h"

#include "generated/settings.h"

#define F_UPDATE_RES        9
#define F_UPDATE            (1<<F_UPDATE_RES)

#define ACCEL_REF_RES       12
#define ACCEL_REF_MAX_PQ    BFP_OF_REAL(128,ACCEL_REF_RES)
#define ACCEL_REF_MAX_R     BFP_OF_REAL( 32,ACCEL_REF_RES)

#define RATE_REF_RES        16
#define RATE_REF_MAX_PQ     BFP_OF_REAL(5,RATE_REF_RES)
#define RATE_REF_MAX_R      BFP_OF_REAL(3,RATE_REF_RES)

#define ANGLE_REF_RES       20
#define PI_ANGLE_REF        BFP_OF_REAL(3.1415926535897932384626433832795029, ANGLE_REF_RES)
#define TWO_PI_ANGLE_REF    BFP_OF_REAL(2.*3.1415926535897932384626433832795029, ANGLE_REF_RES)
#define ANGLE_REF_NORMALIZE(_a) {				\
    while (_a >  PI_ANGLE_REF)  _a -= TWO_PI_ANGLE_REF;		\
    while (_a < -PI_ANGLE_REF)  _a += TWO_PI_ANGLE_REF;		\
  }

extern int32_t booz2_stabilization_cmd[COMMAND_NB];

#endif /* BOOZ2_STABILIZATION_H */
