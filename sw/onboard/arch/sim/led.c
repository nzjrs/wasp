/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 * Copyright (C) 2009 Aaron Marburg <amarburg@notetofutureself.org>
 *
 * This file is part of wasp, some code taken from paparazzi (GPL).
 * This file is forked from John's "null" architecture.
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
/* Simulated implementations of led functions. */

#include "std.h"
#include "debug.h"

#include "led.h"

void led_init ( void ) 
{ 
    DPRINTF("led_init\n");
}

void led_on ( uint8_t id) {}
void led_off ( uint8_t id) {}
void led_toggle ( uint8_t id) {}
void led_check ( uint8_t id) {}
