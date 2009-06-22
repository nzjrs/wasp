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
#include "interrupt_hw.h" 
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

volatile uint8_t            booz2_micromag_status;
volatile int16_t            booz2_micromag_values[MM_NB_AXIS];
volatile uint8_t            booz2_micromag_cur_axe;
uint8_t                     do_booz2_micromag_read;

void
micromag_init(void);

void
micromag_read(void);

static inline void
micromag_reset(void)
{
    booz2_micromag_status = MM_IDLE;
}

static bool_t
micromag_event(void)
{
    return booz2_micromag_status == MM_DATA_AVAILABLE;
}

static void
micromag_schedule_read(void)
{
    do_booz2_micromag_read = TRUE;
}


static inline void
micromag_OnSpiIt(void)
{
    switch (booz2_micromag_status) 
    {
        case MM_SENDING_REQ:
            {
            /* read dummy control byte reply */
            uint8_t foo __attribute__ ((unused)) = SSPDR;
            booz2_micromag_status = MM_WAITING_EOC;
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
	            booz2_micromag_values[booz2_micromag_cur_axe] = new_val;
            MmUnselect();
            SpiClearRti();
            SpiDisableRti();
            SpiDisable();
            booz2_micromag_cur_axe++;
        	if (booz2_micromag_cur_axe > 2)
            {
	            booz2_micromag_cur_axe = 0;
	            booz2_micromag_status = MM_DATA_AVAILABLE;
	        }
	        else
            {
	            booz2_micromag_status = MM_IDLE;
            }
            }
            break;
    }
}

#endif /* _MM_H_FUCK_ */
