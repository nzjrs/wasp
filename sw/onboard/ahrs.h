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
#ifndef BOOZ_AHRS_H
#define BOOZ_AHRS_H

#include "std.h"
#include "math/pprz_algebra_int.h"

typedef struct __AHRS {
  struct Int32Eulers ltp_to_body_euler;
  struct Int32Quat   ltp_to_body_quat;
  struct Int32RMat   ltp_to_body_rmat;
  struct Int32Eulers ltp_to_imu_euler;
  struct Int32Quat   ltp_to_imu_quat;
  struct Int32RMat   ltp_to_imu_rmat;
  struct Int32Rates  imu_rate;
  struct Int32Rates  body_rate;
  bool_t enabled;
} AHRS_t;

extern AHRS_t ahrs;

extern SystemStatus_t ahrs_status;

extern void ahrs_init(void);
extern void ahrs_align(void);
extern void ahrs_propagate(void);
extern void ahrs_update(void);

#endif /* BOOZ_AHRS_H */
