#ifndef _GPIO_H_
#define _GPIO_H_

#include "std.h"

void gpio_init(void);
void gpio_on(uint8_t id);
void gpio_off(uint8_t id);
void gpio_toggle(uint8_t id);
bool_t gpio_get(uint8_t id);
void gpio_periodic_task(void);

#endif /*_GPIO_H_*/
