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

#include "pid_int.h"

#ifndef ABS
#define ABS(a)	   (((a) < 0) ? -(a) : (a))
#endif

#define WINDUP_ON(_pid)         (_pid->features & PID_ENABLE_WINDUP)
#define SAT_MIN_ON(_pid)        (_pid->features & PID_OUTPUT_SAT_MIN)
#define SAT_MAX_ON(_pid)        (_pid->features & PID_OUTPUT_SAT_MAX)
#define HIST_ON(_pid)           (_pid->features & PID_INPUT_HIST)

void pid_enable_feature(PID_t *pid, uint8_t feature, int32_t value)
{
    pid->features |= feature;

    switch (feature) {
        case PID_ENABLE_WINDUP:
            /* integral windup is in absolute output units, so scale to input units */
            pid->intmax = ABS(value / pid->ki);
            break;
        case PID_OUTPUT_SAT_MIN:
            pid->sat_min = value;
            break;
        case PID_OUTPUT_SAT_MAX:
            pid->sat_max = value;
            break;
        case PID_INPUT_HIST:
            break;
    }
}

/**
 *
 * @param pid
 * @param kp
 * @param ki
 * @param kd
 */
void pid_init(PID_t *pid, int32_t kp, int32_t ki, int32_t kd)
{
	pid->kp = kp;
	pid->ki = ki;
	pid->kd = kd;

	pid->sp = 0;
	pid->error_previous = 0;
	pid->integral = 0;

    pid->features = 0;

}

void pid_set(PID_t *pid, int32_t sp)
{
	pid->sp = sp;
	pid->error_previous = 0;
	pid->integral = 0;
}

/**
 *
 * @param pid
 * @param val
 * @param dt
 * @return
 */
int32_t pid_calculate(PID_t *pid, int32_t val, int32_t dt)
{
	int32_t i,d, error, total;

	error = pid->sp - val;
	i = pid->integral + (error * dt);
	d = (error - pid->error_previous) / dt;

    total = (error * pid->kp) + (i * pid->ki) + (d * pid->kd);

    if ( WINDUP_ON(pid) ) {
        if ( i < 0 )
            i = ( i < -pid->intmax ? -pid->intmax : i );
        else
   		    i = ( i < pid->intmax ? i : pid->intmax );
    }
    pid->integral = i;

    if ( SAT_MIN_ON(pid) && (total < pid->sat_min) )
        return pid->sat_min;
    if ( SAT_MAX_ON(pid) && (total > pid->sat_max) )
        return pid->sat_max;

	pid->error_previous = error;
	return total;
}
