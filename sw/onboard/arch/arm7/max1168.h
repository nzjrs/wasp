#ifndef MAX1168_HW_H
#define MAX1168_HW_H

/*
  MAX1168 SPI ADC connected on SPI1 
  SS on P0.20
  EOC on P0.16 ( EINT0 )
*/

#include "std.h"
#include "LPC21xx.h"
#include "arm7/spi_hw.h"

#define MAX1168_ERR_ISR_STATUS      0
#define MAX1168_ERR_READ_OVERUN     1
#define MAX1168_ERR_SPURIOUS_EOC    2

#define MAX1168_SS_PIN              20
#define MAX1168_SS_IODIR            IO0DIR
#define MAX1168_SS_IOSET            IO0SET
#define MAX1168_SS_IOCLR            IO0CLR

#define MAX1168_EOC_PIN             16
#define MAX1168_EOC_PINSEL          PINSEL1
#define MAX1168_EOC_PINSEL_BIT      0
#define MAX1168_EOC_PINSEL_VAL      1
#define MAX1168_EOC_EINT            0

#define MAX1168_NB_CHAN             8

typedef enum {
    MAX1168_IDLE,
    MAX1168_SENDING_REQ,
    MAX1168_READING_RES,
    MAX1168_DATA_AVAILABLE,
} Max1168Status_t;

volatile uint8_t                    max1168_status;
volatile uint16_t                   max1168_values[MAX1168_NB_CHAN];

#define Max1168Unselect()           SetBit(MAX1168_SS_IOSET, MAX1168_SS_PIN)
#define Max1168Select()             SetBit(MAX1168_SS_IOCLR, MAX1168_SS_PIN)

static inline void
max1168_got_interrupt_retrieve_values(void)
{
     /* store convertion result */
    max1168_values[0] = SSPDR;
    max1168_values[1] = SSPDR;
    max1168_values[2] = SSPDR;
    max1168_values[3] = SSPDR;
    max1168_values[4] = SSPDR;
    max1168_values[5] = SSPDR;
    max1168_values[6] = SSPDR;
    max1168_values[7] = SSPDR;

    SpiClearRti();
    SpiDisableRti();
    SpiDisable();
    Max1168Unselect();

    max1168_status = MAX1168_DATA_AVAILABLE;
}

void
max1168_init( void );

void
max1168_read( void );

static inline void
max1168_reset(void)
{
    max1168_status = MAX1168_IDLE;
}

static inline bool_t
max1168_event(void)
{
    return max1168_status == MAX1168_DATA_AVAILABLE;
}

#endif /* MAX1168_HW_H */
