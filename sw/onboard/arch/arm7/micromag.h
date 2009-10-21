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
#ifndef _MM_H_FUCK_
#define _MM_H_FUCK_

/* PNI micromag3 connected on SPI1 
  IMU b2
  SS on P1.28
  RESET on P1.19
  DRDY on P0.30 ( EINT3)
*/

#include <stdlib.h>  // for abs

#include "std.h"
#include "LPC21xx.h"
#include "arm7/spi_hw.h"

#define MM_NB_AXIS          3

#define MM_IDLE             0
#define MM_BUSY             1
#define MM_SENDING_REQ      2
#define MM_WAITING_EOC      3
#define MM_GOT_EOC          4
#define MM_READING_RES      5
#define MM_DATA_AVAILABLE   6

#define MmSelect()          SetBit(MM_SS_IOCLR,MM_SS_PIN)
#define MmUnselect()        SetBit(MM_SS_IOSET,MM_SS_PIN)

#define MmReset()           SetBit(MM_RESET_IOCLR,MM_RESET_PIN)
#define MmSet()             SetBit(MM_RESET_IOSET,MM_RESET_PIN)

volatile uint8_t            micromag_status;
volatile int16_t            micromag_values[MM_NB_AXIS];
volatile uint8_t            micromag_cur_axe;
volatile uint8_t            do_micromag_read;

void
micromag_init(void);

void
micromag_read(void);

static inline void
micromag_reset(void)
{
    micromag_status = MM_IDLE;
}

static inline bool_t
micromag_event(void)
{
    return micromag_status == MM_DATA_AVAILABLE;
}

static inline void
micromag_schedule_read(void)
{
    do_micromag_read = TRUE;
}


static inline void
micromag_got_interrupt_retrieve_values(void)
{
    switch (micromag_status) 
    {
        case MM_SENDING_REQ:
            {
            /* read dummy control byte reply */
            uint8_t foo __attribute__ ((unused)) = SSPDR;
            micromag_status = MM_WAITING_EOC;
            MmUnselect();
            SpiClearRti();
            SpiDisableRti();
            SpiDisable();
            }
            break;
        case MM_READING_RES:
            {
	        int16_t new_val;
            new_val = SSPDR << 8;
            new_val += SSPDR;
            if (abs(new_val) < 2000)
	            micromag_values[micromag_cur_axe] = new_val;
            MmUnselect();
            SpiClearRti();
            SpiDisableRti();
            SpiDisable();
            micromag_cur_axe++;
        	if (micromag_cur_axe > 2)
            {
	            micromag_cur_axe = 0;
	            micromag_status = MM_DATA_AVAILABLE;
	        }
	        else
            {
	            micromag_status = MM_IDLE;
            }
            }
            break;
    }
}

#endif /* _MM_H_FUCK_ */
