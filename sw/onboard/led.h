/*
 * Copyright (C) 2003-2005  Antoine Drouin
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

/** \file led.h
 *  \brief LED (Light Emitting Diodes) API
 *
 *  Assignment of IDs is handeled in settings.xml, for example RC_LED, GPS_LED.
 *  etc. Should ignore LEDs with IDs <= 0
 */

#ifndef LED_H
#define LED_H

#include "std.h"

/**
 * To be called at startup. Backend dependant
 */
void    led_init ( void );

/**
 * Turn on LED
 */
void    led_on ( uint8_t id);

/**
 * Turn off LED
 */
void    led_off ( uint8_t id);

/**
 * Toggle LED
 */
void    led_toggle ( uint8_t id);

/**
 * To be called at periodic frequency. Backend dependant
 */
void    led_periodic_task (void);

/**
 * Printf style debug API. Backend dependant
 */
void    led_log (char const *format, ...) G_GNUC_PRINTF (1, 2);

#endif /* LED_H */
