#include <stdio.h>

#include "std.h"
#include "generated/settings.h"

#include "init.h"
void int_enable(void) {}


#include "sys_time.h"
void sys_time_init(void) {}
void sys_time_chrono_start ( void ) {}
uint32_t sys_time_chrono_stop ( void ) { return 0; }
void sys_time_usleep ( uint32_t us ) {}
void sys_time_calculate_cpu_usage ( void ) {}

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


#include "imu.h"
IMU_t booz_imu;

void imu_init(void) {}
void imu_periodic_task ( void ) {}
uint8_t imu_event_task ( void ) { return 0; }
void imu_adjust_alignment( float phi, float theta, float psi ) {}

#include "gps.h"
SystemStatus_t gps_system_status = STATUS_UNINITIAIZED;
GPS_t gps_state;

void gps_init(void) {}
bool_t gps_event_task(void) { return FALSE; }


