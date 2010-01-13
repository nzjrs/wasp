/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */
#ifndef LED_HW_H
#define LED_HW_H

#include "std.h"

#include "LPC21xx.h"
#include "arm7/config.h"

#define __LED_DIR(i) IO ## i ## DIR
#define _LED_DIR(i) __LED_DIR(i)
#define __LED_CLR(i) IO ## i ## CLR
#define _LED_CLR(i) __LED_CLR(i)
#define __LED_SET(i) IO ## i ## SET
#define _LED_SET(i) __LED_SET(i)
#define __LED_PIN_REG(i) IO ## i ## PIN
#define _LED_PIN_REG(i) __LED_PIN_REG(i)

#define LED_DIR(i) _LED_DIR(LED_ ## i ## _BANK)
#define LED_CLR(i) _LED_CLR(LED_ ## i ## _BANK)
#define LED_SET(i) _LED_SET(LED_ ## i ## _BANK)
#define LED_PIN_REG(i) _LED_PIN_REG(LED_ ## i ## _BANK)
#define LED_PIN(i) LED_ ## i ## _PIN

/* set pin as output */
#define LED_INIT(i)  LED_DIR(i) |= _BV(LED_PIN(i))

#define LED_ON(i) LED_CLR(i) = _BV(LED_PIN(i));
#define LED_OFF(i) LED_SET(i) = _BV(LED_PIN(i));
#define LED_TOGGLE(i) {				\
    if (LED_PIN_REG(i) & _BV(LED_PIN(i)))	\
      LED_ON(i)				        \
    else					\
      LED_OFF(i)				\
}

#endif /* LED_HW_H */
