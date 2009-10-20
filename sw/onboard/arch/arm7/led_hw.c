/*
 * Copyright (C) 2003-2005  Antoine Drouin
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

/** \file led.h
 *  \brief arch independant LED (Light Emitting Diodes) API
 *
 *
 */

#include "led.h"
#include "arm7/led_hw.h"

void led_init ( void ) {
#ifdef LED_1_BANK
  LED_INIT(1);
  LED_OFF(1);
#endif /* LED_1_BANK */

#ifdef LED_2_BANK
  LED_INIT(2);
  LED_OFF(2);
#endif /* LED_2_BANK */

#ifdef LED_3_BANK
  LED_INIT(3);
  LED_OFF(3);
#endif /* LED_3_BANK */

#ifdef LED_4_BANK
  LED_INIT(4);
  LED_OFF(4);
#endif /* LED_4_BANK */

#ifdef LED_5_BANK
  LED_INIT(5);
  LED_OFF(5);
#endif /* LED_5_BANK */

#ifdef LED_6_BANK
  LED_INIT(6);
  LED_OFF(6);
#endif /* LED_6_BANK */

#ifdef LED_7_BANK
  LED_INIT(7);
  LED_OFF(7);
#endif /* LED_7_BANK */

#ifdef LED_8_BANK
  LED_INIT(8);
  LED_OFF(8);
#endif /* LED_8_BANK */
}

void led_on( uint8_t id) {
  switch (id) {
    case 1:
      LED_ON(1);
      break;
    case 2:
      LED_ON(2);
      break;
    case 3:
      LED_ON(3);
      break;
    case 4:
      LED_ON(4);
      break;
    default:
      break;
  }
}

void led_off( uint8_t id) {
  switch (id) {
    case 1:
      LED_OFF(1);
      break;
    case 2:
      LED_OFF(2);
      break;
    case 3:
      LED_OFF(3);
      break;
    case 4:
      LED_OFF(4);
      break;
    default:
      break;
  }
}

void led_toggle( uint8_t id) {
  switch (id) {
    case 1:
      LED_TOGGLE(1);
      break;
    case 2:
      LED_TOGGLE(2);
      break;
    case 3:
      LED_TOGGLE(3);
      break;
    case 4:
      LED_TOGGLE(4);
      break;
    default:
      break;
  }
}


