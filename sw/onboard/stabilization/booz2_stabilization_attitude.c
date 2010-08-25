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
#include "booz2_stabilization_attitude.h"

#include "rc.h"
#include "ahrs.h"
#include "booz2_stabilization.h"

#include "generated/settings.h"

struct Int32Eulers booz_stabilization_att_sp;

struct Int32Eulers booz_stabilization_att_ref;
struct Int32Vect3  booz_stabilization_rate_ref;
struct Int32Vect3  booz_stabilization_accel_ref;

struct Int32Vect3  booz_stabilization_pgain;
struct Int32Vect3  booz_stabilization_dgain;
struct Int32Vect3  booz_stabilization_ddgain;
struct Int32Vect3  booz_stabilization_igain;
struct Int32Eulers booz_stabilization_att_sum_err;

static inline void booz_stabilization_update_ref(void);
static inline void booz_stabilization_attitude_ref_traj_euler_update(void);


void booz2_stabilization_attitude_init(void) {

  INT_EULERS_ZERO(booz_stabilization_att_sp);

  INT_EULERS_ZERO(booz_stabilization_att_ref);
  INT_VECT3_ZERO(booz_stabilization_rate_ref);
  INT_VECT3_ZERO(booz_stabilization_accel_ref);

  VECT3_ASSIGN(booz_stabilization_pgain,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_PGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_PGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PSI_PGAIN);
  
  VECT3_ASSIGN(booz_stabilization_dgain,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PSI_DGAIN);

  VECT3_ASSIGN(booz_stabilization_ddgain,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DDGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DDGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PSI_DDGAIN);

  VECT3_ASSIGN(booz_stabilization_igain,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_IGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_IGAIN,
		    BOOZ_STABILIZATION_ATTITUDE_PSI_IGAIN);

  INT_EULERS_ZERO( booz_stabilization_att_sum_err );

}

#define RC_UPDATE_FREQ  40

void booz2_stabilization_attitude_read_rc(struct Int32Eulers *sp, bool_t in_flight) {

  sp->phi =
    ((int32_t)-rc_values[RADIO_ROLL]  * BOOZ_STABILIZATION_ATTITUDE_SP_MAX_PHI / MAX_PPRZ)
    << (ANGLE_REF_RES - INT32_ANGLE_FRAC);
  sp->theta =
    ((int32_t) rc_values[RADIO_PITCH] * BOOZ_STABILIZATION_ATTITUDE_SP_MAX_THETA / MAX_PPRZ)
    << (ANGLE_REF_RES - INT32_ANGLE_FRAC);
  if (in_flight) {
    if (rc_values[RADIO_YAW] >  BOOZ_STABILIZATION_ATTITUDE_DEADBAND_R ||
        rc_values[RADIO_YAW] < -BOOZ_STABILIZATION_ATTITUDE_DEADBAND_R ) {
        sp->psi +=
            ((int32_t)-rc_values[RADIO_YAW] * BOOZ_STABILIZATION_ATTITUDE_SP_MAX_R / MAX_PPRZ / RC_UPDATE_FREQ)
            << (ANGLE_REF_RES - INT32_ANGLE_FRAC);
        ANGLE_REF_NORMALIZE(sp->psi);
    }
  } else { /* if not flying, use current yaw as setpoint */
    sp->psi = (ahrs.ltp_to_body_euler.psi << (ANGLE_REF_RES - INT32_ANGLE_FRAC));
  }
}

void booz2_stabilization_attitude_enter(void) {

  booz2_stabilization_attitude_reset_psi_ref(  &booz_stabilization_att_sp );
  INT_EULERS_ZERO( booz_stabilization_att_sum_err );
  
}


#define MAX_SUM_ERR 4000000

void booz2_stabilization_attitude_run(bool_t  in_flight) {

  booz_stabilization_update_ref();

  /* compute attitude error            */
  const struct Int32Eulers att_ref_scaled = {
    booz_stabilization_att_ref.phi   >> (ANGLE_REF_RES - INT32_ANGLE_FRAC),
    booz_stabilization_att_ref.theta >> (ANGLE_REF_RES - INT32_ANGLE_FRAC),
    booz_stabilization_att_ref.psi   >> (ANGLE_REF_RES - INT32_ANGLE_FRAC) };
  struct Int32Eulers att_err;
  EULERS_DIFF(att_err, ahrs.ltp_to_body_euler, att_ref_scaled);
  INT32_ANGLE_NORMALIZE(att_err.psi);

  if (in_flight) {
    /* update integrator */
    EULERS_ADD(booz_stabilization_att_sum_err, att_err);
    EULERS_BOUND_CUBE(booz_stabilization_att_sum_err, -MAX_SUM_ERR, MAX_SUM_ERR);
  }
  else {
    INT_EULERS_ZERO(booz_stabilization_att_sum_err);
  }
  
  /* compute rate error                */
  const struct Int32Rates rate_ref_scaled = {
    booz_stabilization_rate_ref.x >> (RATE_REF_RES - INT32_RATE_FRAC),
    booz_stabilization_rate_ref.y >> (RATE_REF_RES - INT32_RATE_FRAC),
    booz_stabilization_rate_ref.z >> (RATE_REF_RES - INT32_RATE_FRAC) };
  struct Int32Rates rate_err;
  RATES_DIFF(rate_err, ahrs.body_rate, rate_ref_scaled);

  /* compute PID loop                  */
  booz2_stabilization_cmd[COMMAND_ROLL] = booz_stabilization_pgain.x    * att_err.phi +
    booz_stabilization_dgain.x    * rate_err.p +
    ((booz_stabilization_ddgain.x * booz_stabilization_accel_ref.x) >> 5) +
    ((booz_stabilization_igain.x  * booz_stabilization_att_sum_err.phi) >> 10);
  booz2_stabilization_cmd[COMMAND_ROLL] = booz2_stabilization_cmd[COMMAND_ROLL] >> 16;

  booz2_stabilization_cmd[COMMAND_PITCH] = booz_stabilization_pgain.y    * att_err.theta +
    booz_stabilization_dgain.y    * rate_err.q +
    ((booz_stabilization_ddgain.y * booz_stabilization_accel_ref.y) >> 5) +
    ((booz_stabilization_igain.y  * booz_stabilization_att_sum_err.theta) >> 10);
  booz2_stabilization_cmd[COMMAND_PITCH] = booz2_stabilization_cmd[COMMAND_PITCH] >> 16;
  
  booz2_stabilization_cmd[COMMAND_YAW] = booz_stabilization_pgain.z    * att_err.psi +
    booz_stabilization_dgain.z    * rate_err.r +
    ((booz_stabilization_ddgain.z * booz_stabilization_accel_ref.z) >> 5) +
    ((booz_stabilization_igain.z  * booz_stabilization_att_sum_err.psi) >> 10);
  booz2_stabilization_cmd[COMMAND_YAW] = booz2_stabilization_cmd[COMMAND_YAW] >> 16;
  
}


/* 

  generation of a saturated linear second order reference trajectory

  roll/pitch
  omega : 1100 deg s-1
  zeta : 0.85
  max rotational accel : 128 rad.s-2  ( ~7300 deg s-2 )
  max rotational speed :   8 rad/s    ( ~ 458 deg s-1 )

  yaw
  omega : 500 deg s-1
  zeta : 0.85
  max rotational accel : 32 rad.s-2  ( ~1833 deg s-2 )
  max rotational speed :  4 rad/s    ( ~ 230 deg s-1 )

  representation
  accel : 20.12
  speed : 16.16 
  angle : 12.20

*/

#define OMEGA_PQ            RadOfDeg(800)
#define ZETA_PQ             0.85
#define ZETA_OMEGA_PQ_RES   10
#define ZETA_OMEGA_PQ       BFP_OF_REAL((ZETA_PQ*OMEGA_PQ), ZETA_OMEGA_PQ_RES)
#define OMEGA_2_PQ_RES      7
#define OMEGA_2_PQ          BFP_OF_REAL((OMEGA_PQ*OMEGA_PQ), OMEGA_2_PQ_RES)
#define OMEGA_R             RadOfDeg(500)
#define ZETA_R              0.85
#define ZETA_OMEGA_R_RES    10
#define ZETA_OMEGA_R        BFP_OF_REAL((ZETA_R*OMEGA_R), ZETA_OMEGA_R_RES)
#define OMEGA_2_R_RES       7
#define OMEGA_2_R           BFP_OF_REAL((OMEGA_R*OMEGA_R), OMEGA_2_R_RES)

static inline void booz_stabilization_attitude_ref_traj_euler_update(void)
{
     /* dumb integrate reference attitude        */
    const struct Int32Eulers d_angle = {
      booz_stabilization_rate_ref.x >> ( F_UPDATE_RES + RATE_REF_RES - ANGLE_REF_RES),
      booz_stabilization_rate_ref.y >> ( F_UPDATE_RES + RATE_REF_RES - ANGLE_REF_RES),
      booz_stabilization_rate_ref.z >> ( F_UPDATE_RES + RATE_REF_RES - ANGLE_REF_RES)};
    EULERS_ADD(booz_stabilization_att_ref, d_angle );
    ANGLE_REF_NORMALIZE(booz_stabilization_att_ref.psi);

    /* integrate reference rotational speeds   */
    const struct Int32Vect3 d_rate = {
      booz_stabilization_accel_ref.x >> ( F_UPDATE_RES + ACCEL_REF_RES - RATE_REF_RES),
      booz_stabilization_accel_ref.y >> ( F_UPDATE_RES + ACCEL_REF_RES - RATE_REF_RES),
      booz_stabilization_accel_ref.z >> ( F_UPDATE_RES + ACCEL_REF_RES - RATE_REF_RES)};
    VECT3_ADD(booz_stabilization_rate_ref, d_rate);

    /* compute reference attitude error        */
    struct Int32Eulers ref_err;
    EULERS_DIFF(ref_err, booz_stabilization_att_ref, booz_stabilization_att_sp);
    /* wrap it in the shortest direction       */
    ANGLE_REF_NORMALIZE(ref_err.psi);

    /* compute reference angular accelerations */
    const struct Int32Vect3 accel_rate = {
      ((int32_t)(-2.*ZETA_OMEGA_PQ)* (booz_stabilization_rate_ref.x >> (RATE_REF_RES - ACCEL_REF_RES))) \
      >> (ZETA_OMEGA_PQ_RES),
      ((int32_t)(-2.*ZETA_OMEGA_PQ)* (booz_stabilization_rate_ref.y >> (RATE_REF_RES - ACCEL_REF_RES))) \
      >> (ZETA_OMEGA_PQ_RES),
      ((int32_t)(-2.*ZETA_OMEGA_R) * (booz_stabilization_rate_ref.z >> (RATE_REF_RES - ACCEL_REF_RES))) \
      >> (ZETA_OMEGA_R_RES) };

    const struct Int32Vect3 accel_angle = {
      ((int32_t)(-OMEGA_2_PQ)* (ref_err.phi   >> (ANGLE_REF_RES - ACCEL_REF_RES))) >> (OMEGA_2_PQ_RES),
      ((int32_t)(-OMEGA_2_PQ)* (ref_err.theta >> (ANGLE_REF_RES - ACCEL_REF_RES))) >> (OMEGA_2_PQ_RES),
      ((int32_t)(-OMEGA_2_R )* (ref_err.psi   >> (ANGLE_REF_RES - ACCEL_REF_RES))) >> (OMEGA_2_R_RES ) };

    VECT3_SUM(booz_stabilization_accel_ref, accel_rate, accel_angle);

    /*	saturate acceleration */
    const struct Int32Vect3 MIN_ACCEL = { -ACCEL_REF_MAX_PQ, -ACCEL_REF_MAX_PQ, -ACCEL_REF_MAX_R };
    const struct Int32Vect3 MAX_ACCEL = {  ACCEL_REF_MAX_PQ,  ACCEL_REF_MAX_PQ,  ACCEL_REF_MAX_R };
    VECT3_BOUND_BOX(booz_stabilization_accel_ref, MIN_ACCEL, MAX_ACCEL);

    /* saturate speed and trim accel accordingly */
    if (booz_stabilization_rate_ref.x >= RATE_REF_MAX_PQ) {
      booz_stabilization_rate_ref.x = RATE_REF_MAX_PQ;
      if (booz_stabilization_accel_ref.x > 0)
	    booz_stabilization_accel_ref.x = 0;
    } else if (booz_stabilization_rate_ref.x <= -RATE_REF_MAX_PQ) {
      booz_stabilization_rate_ref.x = -RATE_REF_MAX_PQ;
      if (booz_stabilization_accel_ref.x < 0)
        booz_stabilization_accel_ref.x = 0;
    }
    if (booz_stabilization_rate_ref.y >= RATE_REF_MAX_PQ) {
      booz_stabilization_rate_ref.y = RATE_REF_MAX_PQ;
      if (booz_stabilization_accel_ref.y > 0)
        booz_stabilization_accel_ref.y = 0;
    } else if (booz_stabilization_rate_ref.y <= -RATE_REF_MAX_PQ) {
      booz_stabilization_rate_ref.y = -RATE_REF_MAX_PQ;
      if (booz_stabilization_accel_ref.y < 0)
        booz_stabilization_accel_ref.y = 0;
    }
    if (booz_stabilization_rate_ref.z >= RATE_REF_MAX_R) {
      booz_stabilization_rate_ref.z = RATE_REF_MAX_R;
      if (booz_stabilization_accel_ref.z > 0)
        booz_stabilization_accel_ref.z = 0;
    } else if (booz_stabilization_rate_ref.z <= -RATE_REF_MAX_R) {
      booz_stabilization_rate_ref.z = -RATE_REF_MAX_R;
      if (booz_stabilization_accel_ref.z < 0)
        booz_stabilization_accel_ref.z = 0;
    }
  }

#define USE_REF         1

static inline void booz_stabilization_update_ref(void)
{

#ifdef USE_REF
  booz_stabilization_attitude_ref_traj_euler_update();
#else
  EULERS_COPY(booz_stabilization_att_ref, booz_stabilization_att_sp);
  INT_VECT3_ZERO(booz_stabilization_rate_ref);
  INT_VECT3_ZERO(booz_stabilization_accel_ref);
#endif

}

void booz2_stabilization_attitude_reset_psi_ref(struct Int32Eulers *sp)
{
    sp->psi = ahrs.ltp_to_body_euler.psi << (ANGLE_REF_RES - INT32_ANGLE_FRAC);
    booz_stabilization_att_ref.psi = sp->psi;
    booz_stabilization_rate_ref.z = 0;
}


