/*
 * Copyright (C) 2005 Pascal Brisset, Antoine Drouin
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

/*
 *\brief ARM7 timing functions 
 *
 */

#ifndef SYS_TIME_HW_H
#define SYS_TIME_HW_H

#include "std.h"

#include "LPC21xx.h"
#include "arm7/config.h"

#include "generated/settings.h"

/* T0 prescaler, set T0_CLK to 15MHz, T0_CLK = PCLK / T0PCLK_DIV */

#if (PCLK == 15000000)
#define T0_PCLK_DIV     1

#elif (PCLK == 30000000)
#define T0_PCLK_DIV     2

#elif (PCLK == 60000000)
#define T0_PCLK_DIV     4

#else
#error unknown PCLK frequency
#endif

#define SYS_TICS_OF_SEC(s)          (uint32_t)(s * PCLK / T0_PCLK_DIV + 0.5)
#define SYS_TICS_OF_USEC(us)        SYS_TICS_OF_SEC((us) * 1e-6)
#define SYS_TICS_OF_NSEC(ns)        SYS_TICS_OF_SEC((ns) * 1e-9)
#define SIGNED_SYS_TICS_OF_SEC(s)   (int32_t)(s * PCLK / T0_PCLK_DIV + 0.5)
#define SIGNED_SYS_TICS_OF_USEC(us) SIGNED_SYS_TICS_OF_SEC((us) * 1e-6)

#define TIME_TICKS_PER_SEC          SYS_TICS_OF_SEC(1)

#define PERIODIC_TASK_PERIOD        SYS_TICS_OF_SEC( PERIODIC_TASK_DT )

#endif /* SYS_TIME_HW_H */
