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
#ifndef _IMU_BABY_H
#define _IMU_BABY_H

#include "std.h"
#include "math/pprz_algebra.h"
#include "math/pprz_algebra_int.h"

typedef struct __IMU {
    float body_to_imu_phi;
    float body_to_imu_theta;
    float body_to_imu_psi;
    struct Int32Rates gyro;
    struct Int32Vect3 accel;
    struct Int32Vect3 mag;
    struct Int32Rates gyro_prev;
    struct Int32Vect3 accel_prev;
    struct Int32Rates gyro_neutral;
    struct Int32Vect3 accel_neutral;
    struct Int32Vect3 mag_neutral;
    struct Int32Rates gyro_unscaled;
    struct Int32Vect3 accel_unscaled;
    struct Int32Vect3 mag_unscaled;
    struct Int32Quat  body_to_imu_quat;
    struct Int32RMat  body_to_imu_rmat;
} IMU_t;

typedef enum {
    IMU_ACC =   1 << 0,
    IMU_GYR =   1 << 1,
    IMU_MAG =   1 << 2
} IMUComponentMast_t;

extern IMU_t booz_imu;

void
imu_init(void);

void
imu_periodic_task ( void );

uint8_t 
imu_event_task ( void );

void
imu_adjust_alignment( float phi, float theta, float psi );

#endif /* _IMU_BABY_H */
