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
/* minimal implementation of all interfaces */
#include "std.h"

#include "init.h"
void int_enable(void) {}
void int_disable(void) {}

#include "rc.h"
SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

void rc_init ( void ) {}
void rc_periodic_task ( void ) {}
bool_t rc_event_task ( void ) { return FALSE; }

#include "imu.h"
IMU_t booz_imu;

void imu_init(void) {}
void imu_periodic_task ( void ) {}
uint8_t imu_event_task ( void ) { return 0; }

#include "actuators.h"
void actuators_init( uint8_t bank ) {}
void actuators_set( ActuatorID_t id, uint8_t value ) {}
void actuators_commit( uint8_t bank ) {}
uint8_t actuators_get_num( uint8_t bank ) { return 0; }

#include "gps.h"
SystemStatus_t gps_system_status = STATUS_UNINITIAIZED;
GPS_t gps_state;

void gps_init(void) {}
bool_t gps_event_task(void) { return FALSE; }

#include "gpio.h"
void gpio_init(void) {}
void gpio_on(uint8_t id) {}
void gpio_off(uint8_t id) {}
void gpio_toggle(uint8_t id) {}
void gpio_periodic_task(void) {}
bool_t gpio_get(uint8_t id) {return FALSE; }

#include "analog.h"
void analog_init( void ) {}
void analog_enable_channel( AnalogChannel_t channel ) {}
uint16_t analog_read_channel( AnalogChannel_t channel ) { return 0; }
uint8_t analog_read_battery( void ) { return 0; }
bool_t analog_event_task( void ) { return FALSE; }
void analog_periodic_task( void ) {}

#include "altimeter.h"
SystemStatus_t altimeter_system_status = STATUS_UNINITIAIZED;
uint16_t altimeter_calibration_offset;
uint16_t altimeter_calibration_raw;

void altimeter_init(void) {}
void altimeter_periodic_task(void) {}
uint8_t altimeter_event_task ( void ) { return 0; }
int32_t altimeter_get_altitude( void ) { return 0; }
void altimeter_recalibrate( void ) {}
