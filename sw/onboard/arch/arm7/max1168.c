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
#include "arm7/armVIC.h"
#include "arm7/max1168.h"

static void EXTINT0_ISR(void) __attribute__((naked));

void max1168_init( void ) {

    /* SS pin is output */
    SetBit(MAX1168_SS_IODIR, MAX1168_SS_PIN);
    /* unselected max1168 */
    Max1168Unselect();

    /* connect P0.16 to extint0 (EOC) */
    MAX1168_EOC_PINSEL |= MAX1168_EOC_PINSEL_VAL << MAX1168_EOC_PINSEL_BIT;
    /* extint0 is edge trigered */
    SetBit(EXTMODE, MAX1168_EOC_EINT);
    /* extint0 is trigered on falling edge */
    ClearBit(EXTPOLAR, MAX1168_EOC_EINT);
    /* clear pending extint0 before enabling interrupts */
    SetBit(EXTINT, MAX1168_EOC_EINT);

    /* initialize interrupt vector */
    VICIntSelect &= ~VIC_BIT( VIC_EINT0 );                     // EXTINT0 selected as IRQ
    VICIntEnable = VIC_BIT( VIC_EINT0 );                       // EXTINT0 interrupt enabled
    _VIC_CNTL(MAX1168_EOC_VIC_SLOT) = VIC_ENABLE | VIC_EINT0;
    _VIC_ADDR(MAX1168_EOC_VIC_SLOT) = (uint32_t)EXTINT0_ISR;   // address of the ISR 

    uint8_t i;
    for (i=0; i<MAX1168_NB_CHAN; i++)
        max1168_values[i] = 0;

    max1168_status = MAX1168_IDLE;
}

void max1168_read( void ) {
    /* select max1168 */ 
    Max1168Select();
    /* enable SPI */
    SpiClearRti();
    SpiDisableRti();
    SpiEnable();
    /* write control byte - wait EOC on extint */
    //  const 
    //uint16_t control_byte = ;
    //  control_byte = control_byte << 8;
    SSPDR = (1 << 0 | 1 << 3 | 7 << 5) << 8;
    max1168_status = MAX1168_SENDING_REQ;
}

void EXTINT0_ISR(void) {
    ISR_ENTRY();
    /* read dummy control byte reply */
    uint16_t foo __attribute__ ((unused));
    foo = SSPDR;
    /* trigger 8 frames read */
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiSend(0);
    SpiClearRti();
    SpiEnableRti();
    max1168_status = MAX1168_READING_RES;

    SetBit(EXTINT, MAX1168_EOC_EINT);   /* clear extint0 */
    VICVectAddr = 0x00000000;           /* clear this interrupt from the VIC */

    ISR_EXIT();
}
