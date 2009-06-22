#include <inttypes.h>

#include "std.h"
#include "init_hw.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"

#include "booz2_imu.h"
#include "booz2_imu_b2.h"

#include "interrupt_hw.h"


static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

static inline void on_imu_event(void);
static inline void on_mag_event(void);

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

  comm_init(COMM_1);

  booz2_imu_impl_init();
  booz2_imu_init();

  int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(COMM_1);

    RunOnceEvery(100, {
        led_toggle(3);
    });

    RunOnceEvery(10, {
        Booz2MicromagScheduleRead();
    });

    booz2_imu_periodic();
}

static inline void main_event_task( void )
{
    comm_event_task(COMM_1);

    Booz2ImuEvent(on_imu_event);
    
    Booz2ImuSpiEvent(booz2_max1168_read,booz2_micromag_read);

    Booz2MicromagEvent(on_mag_event);

}

#define TICKS 30
static inline void on_imu_event(void)
{
    static uint8_t cnt;

    Booz2ImuScaleGyro();
    Booz2ImuScaleAccel();

    if (++cnt > TICKS) cnt = 0;

    if (cnt == 0)
    {
        led_on(2);

        MESSAGE_SEND_IMU_GYRO_RAW(
                COMM_1,
                &booz_imu.gyro_unscaled.p,
                &booz_imu.gyro_unscaled.q,
                &booz_imu.gyro_unscaled.r);

        MESSAGE_SEND_IMU_ACCEL_RAW(
                COMM_1,
                &booz_imu.accel_unscaled.x,
			    &booz_imu.accel_unscaled.y,
			    &booz_imu.accel_unscaled.z);

        MESSAGE_SEND_IMU_MAG_RAW(
                COMM_1,
                &booz_imu.mag_unscaled.x,
			    &booz_imu.mag_unscaled.y,
			    &booz_imu.mag_unscaled.z);
    }
    else if (cnt == (TICKS / 2))
    {
        led_off(2);

        MESSAGE_SEND_WASP_GYRO(
                COMM_1,
                &booz_imu.gyro.p,
                &booz_imu.gyro.q,
                &booz_imu.gyro.r);

        MESSAGE_SEND_WASP_ACCEL(
                COMM_1,
                &booz_imu.accel.x,
                &booz_imu.accel.y,
                &booz_imu.accel.z);

        MESSAGE_SEND_WASP_MAG(
                COMM_1,
                &booz_imu.mag.x,
			    &booz_imu.mag.y,
			    &booz_imu.mag.z);
    }
}

static inline void on_mag_event(void) {
  booz_imu.mag_unscaled.x = booz2_micromag_values[IMU_MAG_X_CHAN];
  booz_imu.mag_unscaled.y = booz2_micromag_values[IMU_MAG_Y_CHAN];
  booz_imu.mag_unscaled.z = booz2_micromag_values[IMU_MAG_Z_CHAN];

  Booz2ImuScaleMag();
}
