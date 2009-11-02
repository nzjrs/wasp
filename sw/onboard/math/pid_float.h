/*
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp
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

#ifndef _PID_FLOAT_H_
#define _PID_FLOAT_H_

#include "std.h"

typedef struct {
		float kp;
		float ki;
		float kd;

		float sp;
		float integral;
		float error_previous;

        unsigned int features;
		float intmax;
        float sat_max;
        float sat_min;
} PID_t;

typedef enum {
    PID_ENABLE_WINDUP   =   (1<<0),
    PID_OUTPUT_SAT_MIN  =   (1<<1),
    PID_OUTPUT_SAT_MAX  =   (1<<2),
    PID_INPUT_HIST      =   (1<<3)
} PIDFeatures_t;

void    pid_init                                    (PID_t          *pid, 
                                                     float          kp, 
                                                     float          ki, 
                                                     float          kd);
void    pid_enable_feature                          (PID_t          *pid, 
                                                     unsigned int   feature,
                                                     float          value);
void    pid_set                                     (PID_t          *pid,
                                                     float          sp);
float   pid_calculate                               (PID_t          *pid,
                                                     float          val,
                                                     float          dt);

#endif /* _PID_FLOAT_H_ */
