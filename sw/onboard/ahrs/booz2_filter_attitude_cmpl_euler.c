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
#include "booz2_filter_attitude_cmpl_euler.h"

#include "imu.h"
#include "ahrs.h"
#include "booz_geometry_mixed.h"
#include "booz_ahrs_aligner.h"

#include "generated/settings.h"

#define BOOZ2_FACE_REINJ_1 1024

AHRS_t ahrs;
SystemStatus_t ahrs_status;

struct Int32Rates  booz2_face_gyro_bias;
struct Int32Eulers booz2_face_measure;
struct Int32Eulers booz2_face_residual;
struct Int32Eulers booz2_face_uncorrected;
struct Int32Eulers booz2_face_corrected;

int32_t booz2_face_reinj_1;

/* 
 * ACC_AMP
 * 9.81 * 2^10 * sin(pi/4) * ACC_AMP = pi/4 * 2^12 * F_UPDATE
 *
 */
#define ACC_AMP 226

#define SAMPLES_NB 256
//static struct booz_ivect lp_gyro_samples[SAMPLES_NB];
//static struct booz_ivect lp_gyro_sum;
static struct booz_ivect lp_accel_samples[SAMPLES_NB];
static struct booz_ivect lp_accel_sum;
static uint8_t samples_idx;


//static inline void apply_alignment(void);

void ahrs_init(void) {
  booz_ahrs_aligner_init();

  ahrs_status = STATUS_UNINITIAIZED;
  INT_EULERS_ZERO(ahrs.ltp_to_body_euler);
  INT_EULERS_ZERO(ahrs.ltp_to_imu_euler);
  INT32_QUAT_ZERO(ahrs.ltp_to_body_quat);
  INT32_QUAT_ZERO(ahrs.ltp_to_body_quat);
  INT_RATES_ZERO(ahrs.body_rate);
  INT_RATES_ZERO(ahrs.imu_rate);
  INT_RATES_ZERO(booz2_face_gyro_bias);
  //  booz2_face_reinj_1 = 1024;
  booz2_face_reinj_1 = BOOZ2_FACE_REINJ_1;
  samples_idx = 0;
}

void ahrs_align(void) {
  if (ahrs_status != STATUS_INITIALIZED) {
    booz_ahrs_aligner_run();
    if (booz_ahrs_aligner.status == BOOZ_AHRS_ALIGNER_LOCKED) {
      RATES_COPY( booz2_face_gyro_bias, booz_ahrs_aligner.lp_gyro);
      ahrs_status = STATUS_INITIALIZED;
    }
    else
      ahrs_status = STATUS_INITIALIZING;
  }
}


#define F_UPDATE 512

#define PI_INTEG_EULER         (PI_INT * F_UPDATE)
#define TWO_PI_INTEG_EULER (TWO_PI_INT * F_UPDATE)
#define INTEG_EULER_NORMALIZE(_a) {				\
    while (_a >  PI_INTEG_EULER)  _a -= TWO_PI_INTEG_EULER;	\
    while (_a < -PI_INTEG_EULER)  _a += TWO_PI_INTEG_EULER;	\
  }


#define PSI_OF_MAG(_psi, _mag, _phi_est, _theta_est) {			\
									\
    int32_t sphi;							\
    BOOZ_ISIN(sphi, _phi_est);						\
    int32_t cphi;							\
    BOOZ_ICOS(cphi, _phi_est);						\
    int32_t stheta;							\
    BOOZ_ISIN(stheta, _theta_est);					\
    int32_t ctheta;							\
    BOOZ_ICOS(ctheta, _theta_est);					\
									\
    int32_t sphi_stheta = BOOZ_IMULT(sphi, stheta, ITRIG_RES );		\
    int32_t cphi_stheta = BOOZ_IMULT(cphi, stheta, ITRIG_RES );		\
    const int32_t mn =							\
      ctheta      * _mag.x+						\
      sphi_stheta * _mag.y+						\
      cphi_stheta * _mag.z;						\
    const int32_t me =							\
      0           * _mag.x+						\
      cphi        * _mag.y+						\
      -sphi       * _mag.z;						\
    float m_psi = -atan2(me, mn);					\
    _psi = ((m_psi)*(float)(1<<(IANGLE_RES))*F_UPDATE);		\
    									\
  }


/*
 *
 * fc = 1/(2*pi*tau)
 *
 * alpha = dt / ( tau + dt )
 *
 *
 *  y(i) = alpha x(i) + (1-alpha) y(i-1)
 *  or
 *  y(i) = y(i-1) + alpha * (x(i) - y(i-1))
 *
 *
 */

void ahrs_propagate(void) {

  /* low pass accels         */
  VECT3_SUB(lp_accel_sum, lp_accel_samples[samples_idx]);
  VECT3_COPY(lp_accel_samples[samples_idx], booz_imu.accel);
  VECT3_ADD(lp_accel_sum, booz_imu.accel);
  samples_idx++;
  //  if (samples_idx > SAMPLES_NB) samples_idx=0;

  /* unbias gyro             */
  struct Int32Rates uf_rate;
  RATES_DIFF(uf_rate, booz_imu.gyro, booz2_face_gyro_bias);
  /* low pass rate */  
  RATES_ADD(ahrs.imu_rate, uf_rate);
  RATES_SDIV(ahrs.imu_rate, ahrs.imu_rate, 2);

  /* dumb integrate eulers */
  struct Int32Eulers euler_dot;
  euler_dot.phi   = ahrs.imu_rate.p;
  euler_dot.theta = ahrs.imu_rate.q;
  euler_dot.psi   = ahrs.imu_rate.r;
  EULERS_ADD(booz2_face_uncorrected, euler_dot);
  EULERS_ADD(booz2_face_corrected, euler_dot);

  /* build a measurement */
  struct Int32Eulers measurement;
  measurement.phi   = -booz_imu.accel.y * ACC_AMP;
  measurement.theta =  booz_imu.accel.x * ACC_AMP;
  PSI_OF_MAG(measurement.psi, booz_imu.mag, 
	     ahrs.ltp_to_imu_euler.phi, ahrs.ltp_to_imu_euler.theta);

  /* low pass it */
  EULERS_ADD(booz2_face_measure, measurement);
  EULERS_SDIV(booz2_face_measure, booz2_face_measure, 2);

  /* compute residual */
  EULERS_DIFF(booz2_face_residual, booz2_face_measure, booz2_face_corrected);
  INTEG_EULER_NORMALIZE(booz2_face_residual.psi);


  struct Int32Eulers correction;
  /* compute a correction */
  EULERS_SDIV(correction, booz2_face_residual, booz2_face_reinj_1);
  /* correct estimation */
  EULERS_ADD(booz2_face_corrected, correction);
  INTEG_EULER_NORMALIZE(booz2_face_corrected.psi);


  /* Compute LTP to IMU eulers      */
  EULERS_SDIV(ahrs.ltp_to_imu_euler, booz2_face_corrected, F_UPDATE);
  /* Compute LTP to IMU quaternion */
  INT32_QUAT_OF_EULERS(ahrs.ltp_to_imu_quat, ahrs.ltp_to_imu_euler);
  /* Compute LTP to IMU rotation matrix */
  INT32_RMAT_OF_EULERS(ahrs.ltp_to_imu_rmat, ahrs.ltp_to_imu_euler);

  /* Compute LTP to BODY quaternion */
  INT32_QUAT_COMP_INV(ahrs.ltp_to_body_quat, booz_imu.body_to_imu_quat, ahrs.ltp_to_imu_quat);
  /* Compute LTP to BODY rotation matrix */
  INT32_RMAT_COMP_INV(ahrs.ltp_to_body_rmat, ahrs.ltp_to_imu_rmat, booz_imu.body_to_imu_rmat);
  /* compute LTP to BODY eulers */
  INT32_EULERS_OF_RMAT(ahrs.ltp_to_body_euler, ahrs.ltp_to_body_rmat);

  /* Do we compute actual body rate ? */
#if 0
  RATES_COPY(ahrs.body_rate, ahrs.imu_rate);
#else
  INT32_RMAT_TRANSP_RATEMULT(ahrs.body_rate, booz_imu.body_to_imu_rmat, ahrs.imu_rate);
#endif
}

void ahrs_update(void) {


}


