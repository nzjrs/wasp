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
#include "booz2_guidance.h"

#include "rc.h"
#include "ins.h"
#include "ahrs.h"
#include "fms.h"

#include "booz2_stabilization.h"
#include "booz2_stabilization_rate.h"
#include "booz2_stabilization_attitude.h"

#include "generated/settings.h"
#include "generated/radio.h"

uint8_t booz2_guidance_h_mode;
uint8_t booz2_guidance_v_mode;

/* horizontal setpoint in NED */
/* Q_int32_xx_8        */
struct Int32Vect2   booz2_guidance_h_pos_sp;
int32_t             booz2_guidance_h_psi_sp;

struct Int32Vect2   booz2_guidance_h_pos_err;
struct Int32Vect2   booz2_guidance_h_speed_err;
struct Int32Vect2   booz2_guidance_h_pos_err_sum;

struct Int32Eulers  booz2_guidance_h_rc_sp;
struct Int32Vect2   booz2_guidance_h_command_earth;
struct Int32Vect2   booz2_guidance_h_stick_earth_sp;
struct Int32Eulers  booz2_guidance_h_command_body;

int32_t             booz2_guidance_h_pgain;
int32_t             booz2_guidance_h_dgain;
int32_t             booz2_guidance_h_igain;

/* direct throttle from radio control (range 0:200 */
int32_t booz2_guidance_v_rc_delta_t;

int32_t booz2_stabilization_cmd[COMMAND_NB];

static inline void booz2_guidance_h_hover_run(void);
static inline void booz2_guidance_h_hover_enter(void);

void booz2_guidance_init(void)
{
    booz2_stabilization_rate_init();
    booz2_stabilization_attitude_init();

    /* horizontal control mode */
    booz2_guidance_h_mode = BOOZ2_GUIDANCE_H_MODE_KILL;
    booz2_guidance_h_psi_sp = 0;
    INT_VECT2_ZERO(booz2_guidance_h_pos_sp);
    INT_VECT2_ZERO(booz2_guidance_h_pos_err_sum);
    INT_EULERS_ZERO(booz2_guidance_h_rc_sp);
    INT_EULERS_ZERO(booz2_guidance_h_command_body);
    booz2_guidance_h_pgain = BOOZ2_GUIDANCE_H_PGAIN;
    booz2_guidance_h_igain = BOOZ2_GUIDANCE_H_IGAIN;
    booz2_guidance_h_dgain = BOOZ2_GUIDANCE_H_DGAIN;

    /* vertical control mode */
    booz2_guidance_v_mode = BOOZ2_GUIDANCE_V_MODE_KILL;
}

void booz2_guidance_mode_changed(uint8_t h_mode, uint8_t v_mode)
{
    bool_t ok;

    /* horizontal control mode */
    if (h_mode != booz2_guidance_h_mode) {
        ok = TRUE;
        switch (h_mode)
        {
            case BOOZ2_GUIDANCE_H_MODE_ATTITUDE:
                booz2_stabilization_attitude_enter();
                break;
            case BOOZ2_GUIDANCE_H_MODE_HOVER:
                booz2_guidance_h_hover_enter();
                break;
            default:
                ok = FALSE;
                break;
        }
        if (ok)
            booz2_guidance_h_mode = h_mode;
    }

    /* vertical control mode */
    if (v_mode != booz2_guidance_v_mode) {
        ok = TRUE;
        switch (v_mode)
        {
            case BOOZ2_GUIDANCE_V_MODE_RC_DIRECT:
                break;
            default:
                ok = FALSE;
        }
        if (ok)
            booz2_guidance_v_mode = v_mode;
    }

}

void booz2_guidance_on_rc_event(bool_t in_flight)
{
    /* horizontal control mode */
    switch ( booz2_guidance_h_mode )
    {
        case BOOZ2_GUIDANCE_H_MODE_RATE:
            booz2_stabilization_rate_read_rc();
            break;
        case BOOZ2_GUIDANCE_H_MODE_ATTITUDE:
            booz2_stabilization_attitude_read_rc(&booz_stabilization_att_sp, in_flight);
            break;
        case BOOZ2_GUIDANCE_H_MODE_HOVER:
            if ( fms_is_enabled() ) {
                EULERS_COPY(booz2_guidance_h_rc_sp, fms.command.h_sp.attitude);
                /* blank out yaw */
                booz2_guidance_h_rc_sp.psi = ahrs.ltp_to_body_euler.psi << (ANGLE_REF_RES - INT32_ANGLE_FRAC);
            } else {
                booz2_stabilization_attitude_read_rc(&booz2_guidance_h_rc_sp, in_flight);
            }
            break;
    }

    /* vertical control mode */
    switch (booz2_guidance_v_mode)
    {
        case BOOZ2_GUIDANCE_V_MODE_RC_DIRECT:
            if ( fms_is_enabled() ) {
                booz2_guidance_v_rc_delta_t = fms.command.v_sp.direct;
            } else {
                booz2_guidance_v_rc_delta_t = (int32_t)rc_values[RADIO_THROTTLE] * 200 / MAX_PPRZ;
            }
            break;
    }
}

void booz2_guidance_run(bool_t in_flight)
{
    /* horizontal control mode */
    switch ( booz2_guidance_h_mode )
    {
    case BOOZ2_GUIDANCE_H_MODE_RATE:
        booz2_stabilization_rate_run(in_flight, booz2_stabilization_cmd);
        break;
    case BOOZ2_GUIDANCE_H_MODE_ATTITUDE:
        booz2_stabilization_attitude_run(in_flight, booz2_stabilization_cmd);
        break;
    case BOOZ2_GUIDANCE_H_MODE_HOVER:
        booz2_guidance_h_hover_run();
        booz2_stabilization_attitude_run(in_flight, booz2_stabilization_cmd);
        break;
    }

    /* vertical control mode */
    switch (booz2_guidance_v_mode)
    {
        case BOOZ2_GUIDANCE_V_MODE_RC_DIRECT:
            booz2_stabilization_cmd[COMMAND_THRUST] = booz2_guidance_v_rc_delta_t;
            break;
    }
}

struct Int32Eulers *
booz2_guidance_sp_get_attitude(void)
{
    /* horizontal control mode */
    switch ( booz2_guidance_h_mode )
    {
        case BOOZ2_GUIDANCE_H_MODE_RATE:
            return NULL;
            break;
        case BOOZ2_GUIDANCE_H_MODE_ATTITUDE:
            return &booz_stabilization_att_sp;
            break;
        case BOOZ2_GUIDANCE_H_MODE_HOVER:
            return &booz2_guidance_h_rc_sp;
            break;
        default:
            return NULL;
            break;
    }
}

#define MAX_POS_ERR         POS_BFP_OF_REAL(16.)
#define MAX_SPEED_ERR       SPEED_BFP_OF_REAL(16.)
#define MAX_POS_ERR_SUM     ((int32_t)(MAX_POS_ERR)<< 12)

// 15 degres
#define MAX_BANK 65536

static inline void  booz2_guidance_h_hover_run(void) {

  /* compute position error */
  VECT2_DIFF(booz2_guidance_h_pos_err, ins.ltp_pos, booz2_guidance_h_pos_sp);
  /* saturate it */
  VECT2_STRIM(booz2_guidance_h_pos_err, -MAX_POS_ERR, MAX_POS_ERR);

  /* compute speed error */
  VECT2_COPY(booz2_guidance_h_speed_err, ins.ltp_speed);
  /* saturate it */
  VECT2_STRIM(booz2_guidance_h_speed_err, -MAX_SPEED_ERR, MAX_SPEED_ERR);
  
  /* update pos error integral */
  VECT2_ADD(booz2_guidance_h_pos_err_sum, booz2_guidance_h_pos_err);
  /* saturate it */
  VECT2_STRIM(booz2_guidance_h_pos_err_sum, -MAX_POS_ERR_SUM, MAX_POS_ERR_SUM);
		    
  /* run PID */
  /* cmd_earth < 15.17 */
  booz2_guidance_h_command_earth.x = (booz2_guidance_h_pgain<<1)  * booz2_guidance_h_pos_err.x +
                                     booz2_guidance_h_dgain * (booz2_guidance_h_speed_err.x>>9) +
                                      booz2_guidance_h_igain * (booz2_guidance_h_pos_err_sum.x >> 12); 
  booz2_guidance_h_command_earth.y = (booz2_guidance_h_pgain<<1)  * booz2_guidance_h_pos_err.y +
                                     booz2_guidance_h_dgain *( booz2_guidance_h_speed_err.y>>9) +
		                      booz2_guidance_h_igain * (booz2_guidance_h_pos_err_sum.y >> 12); 

  VECT2_STRIM(booz2_guidance_h_command_earth, -MAX_BANK, MAX_BANK);

  /* Rotate to body frame */
  int32_t s_psi, c_psi;
  PPRZ_ITRIG_SIN(s_psi, ahrs.ltp_to_body_euler.psi);	
  PPRZ_ITRIG_COS(c_psi, ahrs.ltp_to_body_euler.psi);	


  /* INT32_TRIG_FRAC - 2: 100mm erreur, gain 100 -> 10000 command | 2 degres = 36000, so multiply by 4 */
  booz2_guidance_h_command_body.phi = 
      ( - s_psi * booz2_guidance_h_command_earth.x + c_psi * booz2_guidance_h_command_earth.y)
    >> (INT32_TRIG_FRAC - 2);
  booz2_guidance_h_command_body.theta = 
    - ( c_psi * booz2_guidance_h_command_earth.x + s_psi * booz2_guidance_h_command_earth.y)
    >> (INT32_TRIG_FRAC - 2);


  booz2_guidance_h_command_body.phi   += booz2_guidance_h_rc_sp.phi;
  booz2_guidance_h_command_body.theta += booz2_guidance_h_rc_sp.theta;
  booz2_guidance_h_command_body.psi    = booz2_guidance_h_psi_sp + booz2_guidance_h_rc_sp.psi;
  ANGLE_REF_NORMALIZE(booz2_guidance_h_command_body.psi);

  EULERS_COPY(booz_stabilization_att_sp, booz2_guidance_h_command_body);

}

static inline void booz2_guidance_h_hover_enter(void) {

  VECT2_COPY(booz2_guidance_h_pos_sp, ins.ltp_pos);

  booz2_stabilization_attitude_reset_psi_ref( &booz2_guidance_h_rc_sp );

  INT_VECT2_ZERO(booz2_guidance_h_pos_err_sum);

}

