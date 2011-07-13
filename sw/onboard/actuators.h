/*
 * 
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

/** 
 * @file actuators.h
 * @brief Hardware independent API for actuators (servos, motor controllers)
 *
 * The implementation splits the actuators into 4 banks of 16 actuators.
 * Each bank may be backed by a seperate hw implementation. Nominally, the first
 * bank is for motor controllers, the second bank is for servos,
 * @see ACTUATOR_BANK_MOTORS and @see ACTUATOR_BANK_SERVOS
 * 
 * The ActuatorID_t for a numbered actuator is constructed via (bank_id | actuator_num)
 */
#ifndef ACTUATORS_H
#define ACTUATORS_H

#include "std.h"

typedef uint8_t ActuatorID_t;

/**
 * bank containing motors for the UAV
 */
#define ACTUATOR_BANK_MOTORS            0x10
/**
 * bank containing servos
 */
#define ACTUATOR_BANK_SERVOS            0x20
#define ACTUATOR_BANK_3                 0x40
#define ACTUATOR_BANK_4                 0x80

#define ACTUATOR_BANK_MAX               4
#define ACTUATOR_MAX                    16

/**
 * actuators_init
 *
 * @param bank the bank to initialize
 *
 * @brief initializes the actuators only for the specified bank.
 */
void actuators_init( uint8_t bank );

/**
 * actuators_set
 *
 * @brief sets the supplied actuator to the given value
 */
void actuators_set( ActuatorID_t id, uint8_t value );

/**
 * actuators_commit
 *
 * @param bank actuator bank
 *
 * @brief commits an previously set actuator values to the hardware.
 */
void actuators_commit( uint8_t bank );

/**
 * actuators_get_num
 *
 * @param bank actuator bank
 * @return the number of actuators the hardware backing bank supports
 */
uint8_t actuators_get_num( uint8_t bank );

/**
 * actuators_get
 *
 * @param id
 * @return the value of the actuator corresponding to id
 */
uint8_t actuators_get( ActuatorID_t id );

#endif /* ACTUATORS_H */
