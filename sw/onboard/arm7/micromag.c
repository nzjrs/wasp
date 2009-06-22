#include "arm7/micromag.h"

static void         EXTINT_ISR(void) __attribute__((naked));

void EXTINT_ISR(void) {
    ISR_ENTRY();
    //LED_ON(2);
    booz2_micromag_status = MM_GOT_EOC;
    /* clear EINT */
    SetBit(EXTINT,MM_DRDY_EINT);

    VICVectAddr = 0x00000000;    /* clear this interrupt from the VIC */
    ISR_EXIT();
}

void
micromag_init(void)
{
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
    _VIC_ADDR(MICROMAG_DRDY_VIC_SLOT) = (uint32_t)EXTINT_ISR;         // address of the ISR 

    do_booz2_micromag_read = FALSE;
    booz2_micromag_cur_axe = 0;

    uint8_t i;
    for (i=0; i<MM_NB_AXIS; i++)
        booz2_micromag_values[i] = 0;
    booz2_micromag_status = MM_IDLE;
}

void 
micromag_read(void)
{
    if (booz2_micromag_status == MM_IDLE) 
    {
        MmSelect();
        booz2_micromag_status = MM_SENDING_REQ;
        MmSet();
        SpiClearRti();
        SpiEnableRti();
        uint8_t control_byte = (booz2_micromag_cur_axe+1) << 0 | 3 << 4;
        SSPDR = control_byte;
        MmReset();
        SpiEnable();
    }
    else if (booz2_micromag_status ==  MM_GOT_EOC) 
    {
        booz2_micromag_status = MM_READING_RES;
        MmSelect();
        SpiClearRti();
        SpiEnableRti();
        /* trigger 2 bytes read */
        SSPDR = 0;
        SSPDR = 0;
        SpiEnable();
    }
}


