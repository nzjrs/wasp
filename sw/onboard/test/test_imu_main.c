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
#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "imu.h"
#include "generated/messages.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

static inline void on_imu_event(void);

int main( void ) {
    main_init();
    while(1)
    {
        if (sys_time_periodic())
            main_periodic_task();
        main_event_task();
    }
    return 0;
}

static inline void main_init( void ) {
    hw_init();
    sys_time_init();
    led_init();

    comm_init(COMM_TELEMETRY);

    imu_init();

  int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(COMM_TELEMETRY);
    led_periodic_task();

    RunOnceEvery(100, {
        led_toggle(3);
    });

    imu_periodic_task();

}

#define TICKS 30

static inline void main_event_task( void )
{
    uint8_t valid = 0;
    comm_event_task(COMM_TELEMETRY);

    valid = imu_event_task();
    if ( (valid & IMU_ACC) || (valid & IMU_GYR) ) 
        on_imu_event();

}

static inline void on_imu_event(void)
{
    static uint8_t cnt;

    if (++cnt > TICKS) cnt = 0;

    if (cnt == 0)
    {
        led_on(2);

        MESSAGE_SEND_IMU_GYRO_RAW(
                COMM_TELEMETRY,
                &booz_imu.gyro_unscaled.p,
                &booz_imu.gyro_unscaled.q,
                &booz_imu.gyro_unscaled.r);

        MESSAGE_SEND_IMU_ACCEL_RAW(
                COMM_TELEMETRY,
                &booz_imu.accel_unscaled.x,
			    &booz_imu.accel_unscaled.y,
			    &booz_imu.accel_unscaled.z);

        MESSAGE_SEND_IMU_MAG_RAW(
                COMM_TELEMETRY,
                &booz_imu.mag_unscaled.x,
			    &booz_imu.mag_unscaled.y,
			    &booz_imu.mag_unscaled.z);
    }
    else if (cnt == (TICKS / 2))
    {
        led_off(2);

        MESSAGE_SEND_IMU_GYRO(
                COMM_TELEMETRY,
                &booz_imu.gyro.p,
                &booz_imu.gyro.q,
                &booz_imu.gyro.r);

        MESSAGE_SEND_IMU_ACCEL(
                COMM_TELEMETRY,
                &booz_imu.accel.x,
                &booz_imu.accel.y,
                &booz_imu.accel.z);

        MESSAGE_SEND_IMU_MAG(
                COMM_TELEMETRY,
                &booz_imu.mag.x,
			    &booz_imu.mag.y,
			    &booz_imu.mag.z);
    }
}

