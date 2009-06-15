/*
 * $Id$
 *  
 * Copyright (C) 2008  Antoine Drouin
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

#include <inttypes.h>

#include "init_hw.h"
#include "sys_time.h"
#include "led.h"
#include "interrupt_hw.h"

#include "booz2_commands.h"
#include "i2c.h"
#include "actuators.h"
#include "actuators_buss_twi_blmc_hw.h"

#include "rc.h"

#include "comm.h"
#include "comm-autopilot.h"


#include "booz2_imu.h"
#include "booz2_analog_baro.h"
#include "booz2_battery.h"

#ifdef USE_AMI601
#include "arm7/AMI601.h"
#endif

#include "booz2_fms.h"
#include "booz2_autopilot.h"
#include "booz2_stabilization_rate.h"
#include "booz2_stabilization_attitude.h"

#include "gps.h"
#include "booz2_guidance_h.h"
#include "booz2_guidance_v.h"
#include "booz2_navigation.h"

#include "booz_ahrs_aligner.h"
#include "booz_ahrs.h"
#include "booz2_ins.h"

#include "autopilot_main.h"

static inline void on_imu_event( void );
static inline void on_baro_event( void );
static inline void on_mag_event( void );

uint32_t t0, t1, diff;

int main( void ) {
  booz2_main_init();
  while(1) {
    if (sys_time_periodic())
      booz2_main_periodic();
    booz2_main_event();
  }
  return 0;
}

STATIC_INLINE void booz2_main_init( void ) {
  hw_init();
  sys_time_init();
  led_init();

  i2c_init();
  actuators_init();

  rc_init();

  comm_init(COMM_1);
  comm_add_tx_callback(COMM_1, comm_autopilot_send);

  gps_init();

  booz2_analog_init();
  booz2_analog_baro_init();
  booz2_battery_init();
  booz2_imu_impl_init();
  booz2_imu_init();
#ifdef USE_AMI601
  i2c1_init();
  ami601_init();
#endif

  booz_fms_init();
  booz2_autopilot_init();
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

#ifdef USE_AMI601
#define ReadMag() ami601_read()
#elif USE_MICROMAG
#define ReadMag() Booz2MicromagScheduleRead()
#else
#define ReadMag() {}
#endif

STATIC_INLINE void booz2_main_periodic( void ) {
  //  t0 = T0TC;

  booz2_imu_periodic();
  /* run control loops */
  booz2_autopilot_periodic();
  /* set actuators     */
  SetActuatorsFromCommands(booz2_autopilot_motors_on);

  PeriodicPrescaleBy10(							\
    {						                        \
      rc_periodic_task();		                        \
      if (rc_status != RC_OK)						\
	booz2_autopilot_set_mode(BOOZ2_AP_MODE_FAILSAFE);		\
    },									\
    {									\
        comm_periodic_task(COMM_1);
    },									\
    {									\
      ReadMag();							\
    },									\
    {									\
      booz_fms_periodic();						\
    },									\
    {},									\
    {},									\
    {},									\
    {},									\
    {},									\
    {}									\
    );									\

  //  t1 = T0TC;
  //  diff = t1 - t0;
  //  RunOnceEvery(100, {DOWNLINK_SEND_TIME(&diff);});
  //  t0 = t1;

}

STATIC_INLINE void booz2_main_event( void ) {

  if (rc_event_task())
    booz2_autopilot_on_rc_event();

  Booz2ImuEvent(on_imu_event);

  Booz2AnalogBaroEvent(on_baro_event);

  if (gps_event_task()) {
    if (booz_gps_state.fix == GPS_FIX_3D)
        led_on(GPS_LED);
    else
        led_toggle(GPS_LED);
    booz_ins_update_gps();
  }

#ifdef USE_AMI601
  AMI601Event(on_mag_event);
#endif
#ifdef USE_MICROMAG
  Booz2ImuSpiEvent(booz2_max1168_read,booz2_micromag_read);
  Booz2MicromagEvent(on_mag_event);
#else
  Booz2ImuSpiEvent(booz2_max1168_read);
#endif

  comm_event_task(COMM_1);
}


static inline void on_imu_event( void ) {

  Booz2ImuScaleGyro();
  Booz2ImuScaleAccel();

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

static inline void on_baro_event( void ) {
  booz_ins_update_baro();
}


static inline void on_mag_event(void) {
#ifdef USE_AMI601
  booz_imu.mag_unscaled.x = ami601_val[IMU_MAG_X_CHAN];
  booz_imu.mag_unscaled.y = ami601_val[IMU_MAG_Y_CHAN];
  booz_imu.mag_unscaled.z = ami601_val[IMU_MAG_Z_CHAN];

  Booz2ImuScaleMag();
  ami601_status = AMI601_IDLE;
#endif
#ifdef USE_MICROMAG
  booz_imu.mag_unscaled.x = booz2_micromag_values[IMU_MAG_X_CHAN];
  booz_imu.mag_unscaled.y = booz2_micromag_values[IMU_MAG_Y_CHAN];
  booz_imu.mag_unscaled.z = booz2_micromag_values[IMU_MAG_Z_CHAN];

  Booz2ImuScaleMag();
#endif
}
