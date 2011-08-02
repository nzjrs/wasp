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
#ifndef SERVOS_HW_H
#define SERVOS_HW_H

#include "std.h"
#include "arm7/sys_time_hw.h"

#define SERVOS_TICS_OF_USEC(s)          SYS_TICS_OF_USEC(s)

static inline uint16_t servos_timer_value_from_8bit_range(uint8_t value)
{
    /* value is in range 0 -> 255, so scale this
       range to be in the servo range of 1000 - 2000us */
    uint16_t tmp = ((((uint32_t)value*1000)/0xFF) + 1000);
    return SERVOS_TICS_OF_USEC(tmp);
}

#endif /* SERVOS_HW_H */
