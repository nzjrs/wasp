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
#ifndef _GPIO_HW_
#define _GPIO_HW_

#include "std.h"

#include "LPC21xx.h"
#include "arm7/config.h"

#define __GPIO_DIR(i) IO ## i ## DIR
#define _GPIO_DIR(i) __GPIO_DIR(i)
#define __GPIO_CLR(i) IO ## i ## CLR
#define _GPIO_CLR(i) __GPIO_CLR(i)
#define __GPIO_SET(i) IO ## i ## SET
#define _GPIO_SET(i) __GPIO_SET(i)
#define __GPIO_PIN_REG(i) IO ## i ## PIN
#define _GPIO_PIN_REG(i) __GPIO_PIN_REG(i)

#define GPIO_DIR(i) _GPIO_DIR(GPIO_ ## i ## _BANK)
#define GPIO_CLR(i) _GPIO_CLR(GPIO_ ## i ## _BANK)
#define GPIO_SET(i) _GPIO_SET(GPIO_ ## i ## _BANK)
#define GPIO_PIN_REG(i) _GPIO_PIN_REG(GPIO_ ## i ## _BANK)
#define GPIO_PIN(i) GPIO_ ## i ## _PIN

/* set pin as output */
#define GPIO_INIT(i)  	GPIO_DIR(i) |= _BV(GPIO_PIN(i))
#define GPIO_ON(i) 		GPIO_CLR(i) = _BV(GPIO_PIN(i))
#define GPIO_OFF(i) 	GPIO_SET(i) = _BV(GPIO_PIN(i))
#define GPIO_IS_OFF(i) 	(GPIO_PIN_REG(i) & _BV(GPIO_PIN(i)))
#define GPIO_TOGGLE(i) 	{						\
    if (GPIO_IS_OFF(i))							\
      GPIO_ON(i);				        		\
    else										\
      GPIO_OFF(i);								\
}

#endif /* _GPIO_HW_ */
