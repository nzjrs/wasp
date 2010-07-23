#include "std.h"
#include "generated/settings.h"
#include "nps_led.h"

#include <stdarg.h>
#include <glib.h>
#include <glib/gprintf.h>

static uint8_t leds[LED_NB];

static void led_print(gboolean newline)
{
    g_printf("[%d][%d][%d][%d]%c", leds[0], leds[1], leds[2], leds[3], newline ? '\n' : NULL);
}

void led_init (void)
{
    uint8_t i;
    for (i = 1; i <= LED_NB; i++)
        led_off(i);
}

void led_on (uint8_t id)
{
    leds[id-1] = 1;
    led_print(TRUE);
}

void led_off (uint8_t id)
{
    leds[id-1] = 0;
    led_print(TRUE);
}

void led_toggle (uint8_t id)
{
    leds[id-1] ^= 1;
    led_print(TRUE);
}


gint nps_log (gchar const *format, ...)
{
    va_list args;

    led_print(FALSE);

    va_start (args, format);
    g_vprintf (format, args);
    va_end (args);
}

