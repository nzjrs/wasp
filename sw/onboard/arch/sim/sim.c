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
/* Placeholders providing a minimal implementation of all the arch-
   specific functions */

#include "std.h"

#include "sys_time.h"
uint16_t cpu_time_sec;
uint8_t  cpu_usage;

void sys_time_init( void ) {}
bool_t sys_time_periodic( void ) { return TRUE; }
void sys_time_chrono_start ( void ) {}
uint32_t sys_time_chrono_stop ( void ) { return 0; }
void sys_time_usleep ( uint32_t us ) {}
void sys_time_calculate_cpu_usage ( void ) {}

#include "comm.h"
SystemStatus_t comm_system_status;

void comm_init ( CommChannel_t chan ) {}
bool_t comm_ch_available ( CommChannel_t chan ) { return FALSE; }
void comm_send_ch ( CommChannel_t chan, uint8_t c ) {}
uint8_t comm_get_ch( CommChannel_t chan ) { return '\0'; }
bool_t comm_check_free_space ( CommChannel_t chan, uint8_t len ) { return TRUE; }
void comm_overrun ( CommChannel_t chan ) {}

#include "rc.h"
SystemStatus_t rc_system_status;

void rc_init ( void ) {}
void rc_periodic_task ( void ) {}
bool_t rc_event_task ( void ) { return FALSE; }

#include "imu.h"
void imu_init(void) {}
void imu_periodic_task ( void ) {}
uint8_t imu_event_task ( void ) { return 0; }
void imu_adjust_alignment( float phi, float theta, float psi ) {}

#include "actuators.h"
void actuators_init( uint8_t bank ) {}
void actuators_set( ActuatorID_t id, uint8_t value ) {}
void actuators_commit( uint8_t bank ) {}

#include "gps.h"
SystemStatus_t gps_system_status;
struct Booz_gps_state booz_gps_state;

void gps_init(void) {}
bool_t gps_event_task(void) { return FALSE; }

#include "analog.h"
void analog_init( void ) {}
void analog_enable_channel( AnalogChannel_t channel ) {}
uint16_t analog_read_channel( AnalogChannel_t channel ) { return 0; }
uint8_t analog_read_battery( void ) { return 0; }
bool_t analog_event_task( void ) { return FALSE; }
void analog_periodic_task( void ) {}

#include "altimeter.h"
SystemStatus_t altimeter_system_status;
uint16_t booz2_analog_baro_offset;
uint16_t booz2_analog_baro_value;

void altimeter_init(void) {}
void altimeter_periodic_task(void) {}
uint8_t altimeter_event_task ( void ) { return 0; }
int32_t altimeter_get_altitude( void ) { return 0; }
