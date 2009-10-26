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
