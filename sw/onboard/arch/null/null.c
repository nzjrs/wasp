/* minimal implementation of all interfaces */
#include "std.h"

#include "init.h"
void hw_init(void) {}
void int_enable(void) {}
void int_disable(void) {}

#include "sys_time.h"
uint16_t cpu_time_sec;
void sys_time_init( void ) {}
bool_t sys_time_periodic( void ) { return TRUE; }
void sys_time_chrono_start ( void ) {}
uint32_t sys_time_chrono_stop ( void ) { return 0; }
void sys_time_usleep ( uint32_t us ) {}
void sys_time_calculate_cpu_usage ( void ) {}

#include "led.h"
void led_init ( void ) {}
void led_on ( uint8_t id) {}
void led_off ( uint8_t id) {}
void led_toggle ( uint8_t id) {}
void led_check ( uint8_t id) {}

#include "comm.h"
void comm_init ( CommChannel_t chan ) {}
bool_t comm_ch_available ( CommChannel_t chan ) { return FALSE; }
void comm_send_ch ( CommChannel_t chan, uint8_t c ) {}
uint8_t comm_get_ch( CommChannel_t chan ) { return '\0'; }
bool_t comm_check_free_space ( CommChannel_t chan, uint8_t len ) { return TRUE; }
void comm_overrun ( CommChannel_t chan ) {}

#include "rc.h"
void rc_init ( void ) {}
void rc_periodic_task ( void ) {}
bool_t rc_event_task ( void ) { return FALSE; }

#include "imu.h"
void imu_init(void) {}
void imu_periodic_task ( void ) {}
uint8_t imu_event_task ( void ) { return 0; }

#include "actuators.h"
void actuators_init( uint8_t bank ) {}
void actuators_set( ActuatorID_t id, uint8_t value ) {}
void actuators_commit( uint8_t bank ) {}

#include "gps.h"
struct Booz_gps_state booz_gps_state;

void gps_init(void) {}
bool_t gps_event_task(void) { return FALSE; }

#include "analog.h"
void analog_init( void ) {}

#include "altimeter.h"
SystemStatus_t altimeter_system_status;
uint16_t booz2_analog_baro_offset;
uint16_t booz2_analog_baro_value;

void altimeter_init(void) {}
void altimeter_periodic_task(void) {}
uint8_t altimeter_event_task ( void ) { return 0; }
int32_t altimeter_get_altitude( void ) { return 0; }
