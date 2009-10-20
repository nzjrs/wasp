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
#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "gps.h"
#include "generated/messages.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

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

  comm_init(COMM_1);

  gps_init();

  int_enable();
}

static inline void main_periodic_task( void ) {

  RunOnceEvery(250, {
    MESSAGE_SEND_GPS_LLH( COMM_1, 
        &booz_gps_state.fix,
        &booz_gps_state.num_sv,
        &booz_gps_state.booz2_gps_lat,
        &booz_gps_state.booz2_gps_lon,
        &booz_gps_state.booz2_gps_hmsl,
        &booz_gps_state.booz2_gps_hacc,
        &booz_gps_state.booz2_gps_vacc);
  });


}

static inline void main_event_task( void ) {
    if (gps_event_task()) {
        if (booz_gps_state.fix == GPS_FIX_3D)
            led_on(GPS_LED);
        else
            led_toggle(GPS_LED);
    }
}
