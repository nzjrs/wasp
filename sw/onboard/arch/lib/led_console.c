#include "std.h"
#include "generated/settings.h"

#include "led.h"

#include <stdarg.h>
#include <glib.h>
#include <glib/gprintf.h>

static uint8_t leds[LED_NB];
static char tick[] = {'\\','|','/','-','\\','|','/','-'};
static int tock = 0;

static void led_print(gboolean newline)
{
    g_printf("[%c][%d][%d][%d][%d]%c", tick[tock], leds[0], leds[1], leds[2], leds[3], newline ? '\n' : '\0');
}

void led_init (void)
{
    uint8_t i;
    for (i = 1; i <= LED_NB; i++)
        led_off(i);
}

void led_on (uint8_t id)
{
    uint8_t old = leds[id-1];
    leds[id-1] = 1;
    /* only print if changed */
    if (!old)
        led_print(TRUE);
}

void led_off (uint8_t id)
{
    uint8_t old = leds[id-1];
    leds[id-1] = 0;
    /* only print if changed */
    if (old)
        led_print(TRUE);
}

void led_toggle (uint8_t id)
{
    leds[id-1] ^= 1;
    led_print(TRUE);
}


void led_log (char const *format, ...)
{
    va_list args;

    led_print(FALSE);

    va_start (args, format);
    g_vprintf (format, args);
    va_end (args);
}

void led_periodic_task (void)
{
    RunOnceEvery(100, {
        led_print(TRUE);
        tock = (tock + 1) % (sizeof(tick)/sizeof(char));
    };);
}

