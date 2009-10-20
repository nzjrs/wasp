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

#include "rc.h"

#include "comm.h"
#include "comm_autopilot.h"

#include "imu.h"
#include "analog.h"
#include "altimeter.h"

#include "fms/booz2_fms.h"
#include "autopilot.h"
#include "stabilization/booz2_stabilization_rate.h"
#include "stabilization/booz2_stabilization_attitude.h"

#include "gps.h"
#include "guidance/booz2_guidance_h.h"
#include "guidance/booz2_guidance_v.h"
#include "booz2_navigation.h"

#include "ahrs/booz_ahrs_aligner.h"
#include "booz_ahrs.h"
#include "booz2_ins.h"

#include "autopilot_main.h"

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

  actuators_init(ACTUATOR_BANK_MOTORS);

  rc_init();

  comm_init(COMM_1);
  comm_add_tx_callback(COMM_1, comm_autopilot_message_send);
  comm_add_rx_callback(COMM_1, comm_autopilot_message_received);

  gps_init();

  analog_init();
  analog_enable_channel(ANALOG_CHANNEL_BATTERY);
  analog_enable_channel(ANALOG_CHANNEL_PRESSURE);

  altimeter_init();

  imu_init();

  booz_fms_init();
  autopilot_init();
  booz2_nav_init();
  booz2_guidance_h_init();
  booz2_guidance_v_init();
  booz2_stabilization_rate_init();
  booz2_stabilization_attitude_init();

  booz_ahrs_aligner_init();
  booz_ahrs_init();

  booz_ins_init();

  int_enable();
}

static inline void autopilot_main_periodic( void ) {
  static uint8_t _cnt = 0;

  analog_periodic_task();

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
        if (rc_status == RC_OK)
            led_on(RC_LED);
        else
        {
            led_off(RC_LED);
            autopilot_set_mode(BOOZ2_AP_MODE_FAILSAFE);
        }
        break;
    case 1:
        comm_periodic_task(COMM_1);
        break;
    case 2:
        booz_fms_periodic();
        break;
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
      if (booz_ahrs.status == BOOZ_AHRS_UNINIT) {
        // 150
        booz_ahrs_aligner_run();
        if (booz_ahrs_aligner.status == BOOZ_AHRS_ALIGNER_LOCKED)
          booz_ahrs_align();
      }
      else {
        booz_ahrs_propagate();
        //    booz2_filter_attitude_update();
        
        booz_ins_propagate();
      }
  }

  if ( altimeter_event_task() )
    booz_ins_update_baro();

  if ( gps_event_task() ) {
    if (booz_gps_state.fix == GPS_FIX_3D)
        led_on(GPS_LED);
    else
        led_toggle(GPS_LED);
    booz_ins_update_gps();
  }

  comm_event_task(COMM_1);
}


