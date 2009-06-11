#ifndef RC_HW_H
#define RC_HW_H

#include "std.h"
#include "rc.h"
#include "generated/radio.h"
#include "arm7/sys_time_hw.h"   /* for SYS_TICS_OF_USEC */

#define RC_AVG_PERIOD 8
#define RC_LOST_TIME 30         /* 500ms with a 60Hz timer */
#define RC_REALLY_LOST_TIME 60  /* ~1s */

static inline void ppm_isr ( void ) {
   static uint8_t state = RADIO_CTL_NB;
   static uint32_t last;

    uint32_t now = T0CR2;
    uint32_t length = now - last;
    last = now;

    if (state == RADIO_CTL_NB) {
      if (length > SYS_TICS_OF_USEC(PPM_SYNC_MIN_LEN) &&
	  length < SYS_TICS_OF_USEC(PPM_SYNC_MAX_LEN)) {
	state = 0;
      }
    }
    else {
      if (length > SYS_TICS_OF_USEC(PPM_DATA_MIN_LEN) && 
	  length < SYS_TICS_OF_USEC(PPM_DATA_MAX_LEN)) { 
	ppm_pulses[state] = length; 
	state++; 
	if (state == RADIO_CTL_NB) {
	  ppm_valid = TRUE;
	}
      }
      else
	state = RADIO_CTL_NB;
    }
}

#endif /* RC_HW_H */
