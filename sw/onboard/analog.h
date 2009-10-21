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
#ifndef ANALOG_H
#define ANALOG_H

#include "std.h"

typedef enum {
    ANALOG_CHANNEL_BATTERY = 0,
    ANALOG_CHANNEL_PRESSURE,
    ANALOG_CHANNEL_ADC_SPARE,
    ANALOG_CHANNEL_4,
    ANALOG_CHANNEL_5,
    ANALOG_CHANNEL_6,
    ANALOG_CHANNEL_7,
    ANALOG_CHANNEL_8,
    ANALOG_CHANNEL_NUM
} AnalogChannel_t;

void 
analog_init(void);

void
analog_enable_channel( AnalogChannel_t channel );

/* returns the raw ADC value for the requested channel */
uint16_t
analog_read_channel( AnalogChannel_t channel );

/* returns the battery voltage, in decivolts */
uint8_t
analog_read_battery( void );

bool_t analog_event_task( void );

void analog_periodic_task( void );

#endif /* ANALOG_H */
