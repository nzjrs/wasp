#ifndef _IMU_BABY_H
#define _IMU_BABY_H

#include "std.h"
#include "math/pprz_algebra.h"
#include "math/pprz_algebra_int.h"

/* FIXME: Include these as config/airframe.h
 * For IMU_XXX scale constants */
#include "config/airframe.h"

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

IMU_t               booz_imu;

void
imu_init(void);

void
imu_periodic_task ( void );

uint8_t 
imu_event_task ( void );

void
imu_adjust_alignment( float phi, float theta, float psi );

#endif /* _IMU_BABY_H */
