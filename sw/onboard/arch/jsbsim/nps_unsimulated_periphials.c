#include <stdio.h>

#include "std.h"
#include "config/config.h"

#include "led.h"
static uint8_t leds[NUM_LEDS];

static void led_print(void)
{
    printf("[%d] [%d] [%d] [%d]\n", leds[0], leds[1], leds[2], leds[3]);
}

void led_init (void)
{
    uint8_t i;
    for (i = 1; i <= NUM_LEDS; i++)
        led_off(i);
}

void led_on (uint8_t id)
{
    leds[id-1] = 1;
    led_print();
}

void led_off (uint8_t id)
{
    leds[id-1] = 0;
    led_print();
}

void led_toggle (uint8_t id)
{
    leds[id-1] ^= 1;
    led_print();
}

#include "init.h"
void int_enable(void) {}


#include "sys_time.h"
void sys_time_init(void) {}
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


#include "imu.h"
IMU_t booz_imu;

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


#include "rc.h"
SystemStatus_t rc_system_status;

void rc_init ( void ) {}
void rc_periodic_task ( void ) {}
bool_t rc_event_task ( void ) { return FALSE; }

