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
/* This file has been generated from /home/john/Programming/paparazzi.gitsvn/conf/airframes/booz2_j1.xml */
/* Please DO NOT EDIT */

#ifndef AIRFRAME_H
#define AIRFRAME_H 

#define SECTION_STABILIZATION_RATE 1
#define BOOZ_STABILIZATION_RATE_SP_MAX_P 10000
#define BOOZ_STABILIZATION_RATE_SP_MAX_Q 10000
#define BOOZ_STABILIZATION_RATE_SP_MAX_R 10000
#define BOOZ_STABILIZATION_RATE_GAIN_P -400
#define BOOZ_STABILIZATION_RATE_GAIN_Q -400
#define BOOZ_STABILIZATION_RATE_GAIN_R -350

#define SECTION_STABILIZATION_ATTITUDE 1
#define BOOZ_STABILIZATION_ATTITUDE_SP_MAX_PHI 3000
#define BOOZ_STABILIZATION_ATTITUDE_SP_MAX_THETA 3000
#define BOOZ_STABILIZATION_ATTITUDE_SP_MAX_R 5500
#define BOOZ_STABILIZATION_ATTITUDE_DEADBAND_R 250
#define BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_PGAIN -400
#define BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DGAIN -300
#define BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_DDGAIN  300
#define BOOZ_STABILIZATION_ATTITUDE_PHI_THETA_IGAIN -200
#define BOOZ_STABILIZATION_ATTITUDE_PSI_PGAIN -380
#define BOOZ_STABILIZATION_ATTITUDE_PSI_DGAIN -320
#define BOOZ_STABILIZATION_ATTITUDE_PSI_DDGAIN  300
#define BOOZ_STABILIZATION_ATTITUDE_PSI_IGAIN -75

#define SECTION_GUIDANCE_V 1
#define BOOZ2_GUIDANCE_V_MIN_ERR_Z BOOZ_POS_I_OF_F(-10.)
#define BOOZ2_GUIDANCE_V_MAX_ERR_Z BOOZ_POS_I_OF_F( 10.)
#define BOOZ2_GUIDANCE_V_MIN_ERR_ZD BOOZ_SPEED_I_OF_F(-10.)
#define BOOZ2_GUIDANCE_V_MAX_ERR_ZD BOOZ_SPEED_I_OF_F( 10.)
#define BOOZ2_GUIDANCE_V_HOVER_KP -300
#define BOOZ2_GUIDANCE_V_HOVER_KD -400
#define BOOZ2_GUIDANCE_V_RC_CLIMB_COEF 163
#define BOOZ2_GUIDANCE_V_RC_CLIMB_DEAD_BAND 160000

#define SECTION_GUIDANCE_H 1
#define BOOZ2_GUIDANCE_H_PGAIN -20
#define BOOZ2_GUIDANCE_H_DGAIN -0
#define BOOZ2_GUIDANCE_H_IGAIN -5

#define SECTION_MISC 1
#define BOOZ2_FACE_REINJ_1 1024

#endif // AIRFRAME_H
