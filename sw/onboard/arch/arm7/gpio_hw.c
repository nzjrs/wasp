#include "std.h"
#include "gpio.h"

#include "LPC21xx.h"
#include "arm7/config.h"
#include "arm7/gpio_hw.h"
#include "generated/settings.h"

SystemStatus_t gpio_system_status = STATUS_UNINITIAIZED;

void gpio_init(void)
{
    if (gpio_system_status == STATUS_INITIALIZED)
        return;

#ifdef GPIO_1_BANK
    GPIO_INIT(1);
    GPIO_OFF(1);
#endif

#ifdef GPIO_2_BANK
    GPIO_INIT(2);
    GPIO_OFF(2);
#endif

#ifdef GPIO_3_BANK
    GPIO_INIT(3);
    GPIO_OFF(3);
#endif

#ifdef GPIO_4_BANK
    GPIO_INIT(4);
    GPIO_OFF(4);
#endif

#ifdef GPIO_5_BANK
    GPIO_INIT(5);
    GPIO_OFF(5);
#endif

#ifdef GPIO_6_BANK
    GPIO_INIT(6);
    GPIO_OFF(6);
#endif

#ifdef GPIO_7_BANK
    GPIO_INIT(7);
    GPIO_OFF(7);
#endif

#ifdef GPIO_8_BANK
    GPIO_INIT(8);
    GPIO_OFF(8);
#endif

    gpio_system_status = STATUS_INITIALIZED;
}

void gpio_on(uint8_t id)
{
    switch (id) {
#ifdef GPIO_1_BANK
        case 1:
            GPIO_ON(1);
            break;
#endif
#ifdef GPIO_2_BANK
        case 2:
            GPIO_ON(2);
            break;
#endif
#ifdef GPIO_3_BANK
        case 3:
            GPIO_ON(3);
            break;
#endif
#ifdef GPIO_4_BANK
        case 4:
            GPIO_ON(4);
            break;
#endif
#ifdef GPIO_5_BANK
        case 5:
            GPIO_ON(5);
            break;
#endif
#ifdef GPIO_6_BANK
        case 6:
            GPIO_ON(6);
            break;
#endif
#ifdef GPIO_7_BANK
        case 7:
            GPIO_ON(7);
            break;
#endif
#ifdef GPIO_8_BANK
        case 8:
            GPIO_ON(8);
            break;
#endif
        default:
            break;
    }
}

void gpio_off(uint8_t id)
{
    switch (id) {
#ifdef GPIO_1_BANK
        case 1:
            GPIO_OFF(1);
            break;
#endif
#ifdef GPIO_2_BANK
        case 2:
            GPIO_OFF(2);
            break;
#endif
#ifdef GPIO_3_BANK
        case 3:
            GPIO_OFF(3);
            break;
#endif
#ifdef GPIO_4_BANK
        case 4:
            GPIO_OFF(4);
            break;
#endif
#ifdef GPIO_5_BANK
        case 5:
            GPIO_OFF(5);
            break;
#endif
#ifdef GPIO_6_BANK
        case 6:
            GPIO_OFF(6);
            break;
#endif
#ifdef GPIO_7_BANK
        case 7:
            GPIO_OFF(7);
            break;
#endif
#ifdef GPIO_8_BANK
        case 8:
            GPIO_OFF(8);
            break;
#endif
        default:
            break;
    }
}

void gpio_toggle(uint8_t id)
{
    switch (id) {
#ifdef GPIO_1_BANK
        case 1:
            GPIO_TOGGLE(1);
            break;
#endif
#ifdef GPIO_2_BANK
        case 2:
            GPIO_TOGGLE(2);
            break;
#endif
#ifdef GPIO_3_BANK
        case 3:
            GPIO_TOGGLE(3);
            break;
#endif
#ifdef GPIO_4_BANK
        case 4:
            GPIO_TOGGLE(4);
            break;
#endif
#ifdef GPIO_5_BANK
        case 5:
            GPIO_TOGGLE(5);
            break;
#endif
#ifdef GPIO_6_BANK
        case 6:
            GPIO_TOGGLE(6);
            break;
#endif
#ifdef GPIO_7_BANK
        case 7:
            GPIO_TOGGLE(7);
            break;
#endif
#ifdef GPIO_8_BANK
        case 8:
            GPIO_TOGGLE(8);
            break;
#endif
        default:
            break;
    }
}

void gpio_periodic_task(void)
{

}

bool_t gpio_get(uint8_t id)
{

    switch (id) {
#ifdef GPIO_1_BANK
        case 1:
            return !GPIO_IS_OFF(1);
            break;
#endif
#ifdef GPIO_2_BANK
        case 2:
            return !GPIO_IS_OFF(2);
            break;
#endif
#ifdef GPIO_3_BANK
        case 3:
            return !GPIO_IS_OFF(3);
            break;
#endif
#ifdef GPIO_4_BANK
        case 4:
            return !GPIO_IS_OFF(4);
            break;
#endif
#ifdef GPIO_5_BANK
        case 5:
            return !GPIO_IS_OFF(5);
            break;
#endif
#ifdef GPIO_6_BANK
        case 6:
            return !GPIO_IS_OFF(6);
            break;
#endif
#ifdef GPIO_7_BANK
        case 7:
            return !GPIO_IS_OFF(7);
            break;
#endif
#ifdef GPIO_8_BANK
        case 8:
            return !GPIO_IS_OFF(8);
            break;
#endif
        default:
            return FALSE;
            break;
    }
}

