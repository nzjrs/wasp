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
#ifndef SYS_TIME_H
#define SYS_TIME_H

#include "std.h"

/* the number of seconds the CPU has been running */
extern uint16_t cpu_time_sec;

/* the estimated CPU usages, percent, 0-100 */
extern uint8_t  cpu_usage;

void
sys_time_init( void );

bool_t 
sys_time_periodic( void );

void
sys_time_chrono_start ( void );

uint32_t 
sys_time_chrono_stop ( void );

void
sys_time_usleep ( uint32_t us );

uint32_t
sys_time_get_ticks(void);

/**
 * Calculates an approximation of the CPU usage, assuming
 * this function is called immediately before 
 * sys_time_get_periodic.
 */
void sys_time_calculate_cpu_usage ( void );

#endif /* SYS_TIME_H */
