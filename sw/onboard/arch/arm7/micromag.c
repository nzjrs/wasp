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
#include "arm7/micromag.h"

static void         EXTINT_ISR(void) __attribute__((naked));

void EXTINT_ISR(void) 
{
    ISR_ENTRY();
    micromag_status = MM_GOT_EOC;
    /* clear EINT */
    SetBit(EXTINT,MM_DRDY_EINT);
    VICVectAddr = 0x00000000;    /* clear this interrupt from the VIC */
    ISR_EXIT();
}

void
micromag_init(void)
{
    uint8_t i;

    /* configure SS pin */
    SetBit(MM_SS_IODIR, MM_SS_PIN); /* pin is output  */
    MmUnselect();                   /* pin idles high */

    /* configure RESET pin */
    SetBit(MM_RESET_IODIR, MM_RESET_PIN); /* pin is output  */
    MmReset();                            /* pin idles low  */

    /* configure DRDY pin */
    /* connected pin to EXINT */ 
    MM_DRDY_PINSEL |= MM_DRDY_PINSEL_VAL << MM_DRDY_PINSEL_BIT;
    SetBit(EXTMODE, MM_DRDY_EINT); /* EINT is edge trigered */
    SetBit(EXTPOLAR,MM_DRDY_EINT); /* EINT is trigered on rising edge */
    SetBit(EXTINT,MM_DRDY_EINT);   /* clear pending EINT */

    /* initialize interrupt vector */
    VICIntSelect &= ~VIC_BIT( MM_DRDY_VIC_IT );                       /* select EINT as IRQ source */
    VICIntEnable = VIC_BIT( MM_DRDY_VIC_IT );                         /* enable it                 */
    _VIC_CNTL(MICROMAG_DRDY_VIC_SLOT) = VIC_ENABLE | MM_DRDY_VIC_IT;
    _VIC_ADDR(MICROMAG_DRDY_VIC_SLOT) = (uint32_t)EXTINT_ISR;         /* address of the ISR */

    do_micromag_read = FALSE;
    micromag_cur_axe = 0;

    for (i=0; i<MM_NB_AXIS; i++)
        micromag_values[i] = 0;
    micromag_status = MM_IDLE;
}

void 
micromag_read(void)
{
    if (micromag_status == MM_IDLE) 
    {
        uint8_t control_byte;

        MmSelect();
        micromag_status = MM_SENDING_REQ;
        MmSet();
        SpiClearRti();
        SpiEnableRti();
        control_byte = (micromag_cur_axe+1) << 0 | 3 << 4;
        SpiSend(control_byte);
        MmReset();
        SpiEnable();
    }
    else if (micromag_status ==  MM_GOT_EOC) 
    {
        micromag_status = MM_READING_RES;
        MmSelect();
        SpiClearRti();
        SpiEnableRti();
        /* trigger 2 bytes read */
        SpiSend(0);
        SpiSend(0);
        SpiEnable();
    }
}

