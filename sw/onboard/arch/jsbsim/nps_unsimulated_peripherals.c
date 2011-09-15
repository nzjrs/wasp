#include <stdio.h>

#include "std.h"
#include "generated/settings.h"

#include "init.h"
void int_enable(void) {}


#include "sys_time.h"
void sys_time_init(void) {}
void sys_time_chrono_start ( void ) {}
uint32_t sys_time_chrono_stop ( void ) { return 0; }
uint32_t sys_time_get_ticks ( void ) { return 0; }
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
uint8_t analog_read_battery( void ) { return 120; }
bool_t analog_event_task( void ) { return FALSE; }
void analog_periodic_task( void ) {}


