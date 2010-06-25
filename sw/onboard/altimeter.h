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
#ifndef ALTIMETER_H
#define ALTIMETER_H

#include "std.h"

extern SystemStatus_t altimeter_system_status;

extern uint16_t altimeter_calibration_offset;
extern uint16_t altimeter_calibration_raw;

void
altimeter_init(void);

void
altimeter_periodic_task(void);

uint8_t 
altimeter_event_task ( void );

int32_t
altimeter_get_altitude( void );

void
altimeter_recalibrate( void );

#endif /* ALTIMETER_H */
