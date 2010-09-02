/*
 * Copyright (C) 2008  Antoine Drouin
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

#include <inttypes.h>

#include "init.h"
#include "sys_time.h"
#include "led.h"

#include "actuators.h"
#include "supervision.h"

#include "rc.h"

#include "comm.h"
#include "comm_autopilot.h"

#include "imu.h"
#include "analog.h"
#include "altimeter.h"

#include "autopilot.h"
#include "stabilization.h"

#include "gps.h"
#include "guidance.h"
//#include "booz2_navigation.h"

#include "ahrs.h"
#include "ins.h"

#include "fms.h"

#include "autopilot_main.h"

#include "generated/settings.h"

int main( void ) {
    autopilot_main_init();
    while(1) {
        if (sys_time_periodic()) {
            autopilot_main_periodic();
            sys_time_calculate_cpu_usage();
        }
        autopilot_main_event();
    }
    return 0;
}

static inline void autopilot_main_init( void ) {
  hw_init();
  sys_time_init();
  led_init();

  supervision_init();
  actuators_init(ACTUATOR_BANK_SERVOS);

  rc_init();

  comm_init(COMM_TELEMETRY);
  comm_add_tx_callback(COMM_TELEMETRY, comm_autopilot_message_send);
  comm_add_rx_callback(COMM_TELEMETRY, comm_autopilot_message_received);

  gps_init();

  analog_init();
  analog_enable_channel(ANALOG_CHANNEL_BATTERY);
  analog_enable_channel(ANALOG_CHANNEL_PRESSURE);

  altimeter_init();

  imu_init();

  autopilot_init();
  guidance_init();
  stabilization_init();

  ahrs_init();
  ins_init();

  fms_init();

  int_enable();
}

static inline void autopilot_main_periodic( void ) {
  static uint8_t _cnt = 0;

  /* read analog baro */
  analog_periodic_task();
  altimeter_periodic_task();

  /* read imu */
  imu_periodic_task();

  /* run control loops */
  autopilot_periodic();
  /* set actuators     */
  autopilot_set_actuators();

  /* Run the following tasks 10x times slower than the periodic rate */
  _cnt++;
  if (_cnt >= 10)
    _cnt = 0;
  switch (_cnt)
  {
    case 0:
        rc_periodic_task();
        if (rc_status == RC_OK) {
            led_on(LED_RC);
        } else {
            led_off(LED_RC);
            autopilot_set_mode(AP_MODE_FAILSAFE);
        }
        break;
    case 1:
        comm_periodic_task(COMM_TELEMETRY);
        break;
    case 2:
        fms_periodic_task();
        break;
  }

  /* flash leds... */
  led_periodic_task();

  if (ahrs_status == STATUS_INITIALIZING) {
    RunOnceEvery(50, {
      led_toggle(LED_AHRS);
    });
  } else if (ahrs_status == STATUS_INITIALIZED) {
    led_on(LED_AHRS);
  }
  if (altimeter_system_status == STATUS_INITIALIZING) {
    RunOnceEvery(50, {
      led_toggle(LED_BARO);
    });
  } else if (altimeter_system_status == STATUS_INITIALIZED) {
    led_on(LED_BARO);
  }

}

static inline void autopilot_main_event( void ) {
  uint8_t valid = 0;

  analog_event_task();

  if (rc_event_task())
    autopilot_on_rc_event();

  valid = imu_event_task();
  if ( (valid & IMU_ACC) || (valid & IMU_GYR) ) 
  {
      if (ahrs_status != STATUS_INITIALIZED) {
        ahrs_align();
      }
      else {
        ahrs_propagate();
        ins_propagate();
      }
  }

  if ( altimeter_event_task() )
    ins_update_baro();

  if ( gps_event_task() ) {
    if (gps_state.fix == GPS_FIX_3D)
        led_on(LED_GPS);
    else
        led_toggle(LED_GPS);
    ins_update_gps();
  }

  comm_event_task(COMM_TELEMETRY);
}


