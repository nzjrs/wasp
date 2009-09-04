/*  $Id$
 *
 * (c) 2003-2005 Pascal Brisset, Antoine Drouin
 *
 * This file is part of paparazzi.
 *
 * paparazzi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * paparazzi is distributed in the hope that it will be useful,
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

/** \file actuators.h
 *  \brief Hardware independent API for actuators (servos, motor controllers)
 *
 *  The implementation splits the actuators into 4 banks of 16 actuators.
 *  nominally, the first bank is for motor controllers, the second bank is
 *  for servos
 */
#ifndef ACTUATORS_H
#define ACTUATORS_H

#include "std.h"

typedef uint8_t ActuatorID_t;

#define ACTUATOR_BANK_MOTORS            0x10
#define ACTUATOR_BANK_SERVOS            0x20
#define ACTUATOR_BANK_3                 0x40
#define ACTUATOR_BANK_4                 0x80

void actuators_init( uint8_t bank );

void actuators_set( ActuatorID_t id, uint8_t value );

void actuators_commit( uint8_t bank );

#endif /* ACTUATORS_H */
