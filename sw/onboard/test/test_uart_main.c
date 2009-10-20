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
#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

#define USE_DA_USB 0
#define USE_DA_UART0 1
#define USE_DA_UART1 1


int main( void ) {
  main_init();
  while(1) {
    if (sys_time_periodic())
      main_periodic_task();
    main_event_task();
  }
  return 0;
}

static inline void main_init( void ) {
  hw_init();
  sys_time_init();
  led_init();

#if USE_DA_UART0
  /* Uart 0 (aka gps) */
  comm_init(COMM_0);
#endif

#if USE_DA_UART1
  /* Uart 1 (aka telemetry) */
  comm_init(COMM_1);
#endif

#if USE_DA_USB
  /* USB */
  comm_init(COMM_USB);
#endif

  int_enable();
}

static inline void main_periodic_task( void ) {
    static uint8_t c = 'a';

  RunOnceEvery(200, {
    led_toggle(4);

#if USE_DA_UART0
    comm_send_ch(COMM_0, c);
#endif

#if USE_DA_UART1
    comm_send_ch(COMM_1, c);
#endif

#if USE_DA_USB
    comm_send_ch(COMM_USB, c);
#endif

    c = (c < 'z' ? c + 1 : 'a');

  });

}

static inline void main_event_task( void ) {

}
