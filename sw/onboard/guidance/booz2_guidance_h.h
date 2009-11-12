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
#ifndef BOOZ2_GUIDANCE_H_H
#define BOOZ2_GUIDANCE_H_H

#include "guidance.h"
#include "math/pprz_algebra_int.h"

/* horizontal setpoint in NED */
/* Q_int32_xx_8        */
extern struct Int32Vect2 booz2_guidance_h_pos_sp;
extern int32_t           booz2_guidance_h_psi_sp;

extern struct Int32Vect2 booz2_guidance_h_pos_err;
extern struct Int32Vect2 booz2_guidance_h_speed_err;
extern struct Int32Vect2 booz2_guidance_h_pos_err_sum;

extern struct Int32Eulers booz2_guidance_h_rc_sp;
extern struct Int32Vect2 booz2_guidance_h_command_earth;
extern struct Int32Eulers booz2_guidance_h_command_body;

extern int32_t booz2_guidance_h_pgain;
extern int32_t booz2_guidance_h_dgain;
extern int32_t booz2_guidance_h_igain;


extern void booz2_guidance_h_init(void);
extern void booz2_guidance_h_mode_changed(uint8_t new_mode);
extern void booz2_guidance_h_read_rc(bool_t  in_flight);
extern void booz2_guidance_h_run(bool_t  in_flight);


#define booz2_guidance_h_SetKi(_val) {			\
    booz2_guidance_h_igain = _val;			\
    INT_VECT2_ZERO(booz2_guidance_h_pos_err_sum);	\
  }

#endif /* BOOZ2_GUIDANCE_H_H */
