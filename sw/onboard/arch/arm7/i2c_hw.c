/*
 * Copyright (C) 2008  Pascal Brisset, Antoine Drouin
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
#include "config/config.h"

#include "LPC21xx.h"
#include "arm7/armVIC.h"
#include "arm7/i2c_hw.h"

/* default clock speed 37.5KHz with our 15MHz PCLK 
   I2C0_CLOCK = PCLK / (I2C0_SCLL + I2C0_SCLH)     */

/* adjust for other PCLKs */

#if (PCLK == 15000000)
#define I2C0_SCLL_D I2C0_SCLL
#define I2C0_SCLH_D I2C0_SCLH
#define I2C1_SCLL_D I2C1_SCLL
#define I2C1_SCLH_D I2C1_SCLH
#else

#if (PCLK == 30000000)
#define I2C0_SCLL_D (2*I2C0_SCLL)
#define I2C0_SCLH_D (2*I2C0_SCLH)
#define I2C1_SCLL_D (2*I2C1_SCLL)
#define I2C1_SCLH_D (2*I2C1_SCLH)
#else

#if (PCLK == 60000000)
#define I2C0_SCLL_D (4*I2C0_SCLL)
#define I2C0_SCLH_D (4*I2C0_SCLH)
#define I2C1_SCLL_D (4*I2C1_SCLL)
#define I2C1_SCLH_D (4*I2C1_SCLH)
#else

#error unknown PCLK frequency
#endif
#endif
#endif

#define I2C_START           0x08
#define I2C_RESTART         0x10
#define I2C_MT_SLA_ACK      0x18
#define I2C_MT_SLA_NACK     0x20
#define I2C_MT_DATA_ACK     0x28
#define I2C_MR_SLA_ACK      0x40
#define I2C_MR_SLA_NACK     0x48
#define I2C_MR_DATA_ACK     0x50
#define I2C_MR_DATA_NACK    0x58

#define I2C_IDLE            0
#define I2C_BUSY            1
#define I2C_RECEIVE         1

#if USE_I2C0

volatile uint8_t i2c_status;
volatile uint8_t i2c_buf[I2C_BUF_LEN];
volatile uint8_t i2c_len;
volatile uint8_t i2c_index;
volatile uint8_t i2c_slave_addr;
volatile bool_t* i2c_finished;
volatile I2cStopCallback_t i2c_stop_callback;

#define I2C_DATA_REG I2C0DAT
#define I2C_STATUS_REG I2C0STAT

#define I2cSendAck()   { I2C0CONSET = _BV(AA); }
#define I2cSendStop()  {						\
    I2C0CONSET = _BV(STO);						\
    if (i2c_finished) *i2c_finished = TRUE;				\
    i2c_status = I2C_IDLE;						\
    if (i2c_stop_callback)						\
		i2c_stop_callback();					\
  }
#define I2cSendStart() { I2C0CONSET = _BV(STA); }
#define I2cSendByte(b) { I2C_DATA_REG = b; }

#define I2cReceive(_ack) {	    \
    if (_ack) I2C0CONSET = _BV(AA); \
    else I2C0CONCLR = _BV(AAC);	    \
  }

#define I2cClearStart() { I2C0CONCLR = _BV(STAC); }
#define I2cClearIT() { I2C0CONCLR = _BV(SIC); }

void i2c0_ISR(void) __attribute__((naked));
static inline void i2c_automaton(uint32_t state);

void i2c0_ISR(void)
{
    ISR_ENTRY();

    uint32_t state = I2C_STATUS_REG;

    i2c_automaton(state);
    I2cClearIT();

    VICVectAddr = 0x00000000;             // clear this interrupt from the VIC
    ISR_EXIT();                           // recover registers and return
}

/* SDA0 on P0.3 */
/* SCL0 on P0.2 */
void i2c_init(void) {
    /* set P0.2 and P0.3 to I2C0 */
    PINSEL0 |= 1 << 4 | 1 << 6;
    /* clear all flags */
    I2C0CONCLR = _BV(AAC) | _BV(SIC) | _BV(STAC) | _BV(I2ENC);
    /* enable I2C */
    I2C0CONSET = _BV(I2EN);
    /* set bitrate */
    I2C0SCLL = I2C0_SCLL_D;  
    I2C0SCLH = I2C0_SCLH_D;  

    // initialize the interrupt vector
    VICIntSelect &= ~VIC_BIT(VIC_I2C0);              // I2C0 selected as IRQ
    VICIntEnable = VIC_BIT(VIC_I2C0);                // I2C0 interrupt enabled
    _VIC_CNTL(I2C0_VIC_SLOT) = VIC_ENABLE | VIC_I2C0;
    _VIC_ADDR(I2C0_VIC_SLOT) = (uint32_t)i2c0_ISR;    // address of the ISR

    i2c_status = I2C_IDLE;
    i2c_finished = 0;
    i2c_stop_callback = 0;
}

void i2c_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished) {
    i2c_len = len;
    i2c_slave_addr = slave_addr | I2C_RECEIVE;
    i2c_finished = finished;
    i2c_status = I2C_BUSY;
    I2cSendStart();
}

void i2c_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished) {
    i2c_len = len;
    i2c_slave_addr = slave_addr & ~I2C_RECEIVE;
    i2c_finished = finished;
    i2c_status = I2C_BUSY;
    I2cSendStart();
}

static inline void i2c_automaton(uint32_t state)
{
    switch (state) {
        case I2C_START:
        case I2C_RESTART:
            I2cSendByte(i2c_slave_addr);
            I2cClearStart();
            i2c_index = 0;
            break;
        case I2C_MR_DATA_ACK:
            if (i2c_index < i2c_len) {
	            i2c_buf[i2c_index] = I2C_DATA_REG;
	            i2c_index++;
	            I2cReceive(i2c_index < i2c_len - 1);
            } 
            else {
	            /* error , we should have got NACK */
            	I2cSendStop();
            }
            break;
        case I2C_MR_SLA_ACK: /* At least one char */
            /* Wait and reply with ACK or NACK */
            I2cReceive(i2c_index < i2c_len - 1);
            break;
        case I2C_MR_SLA_NACK:
        case I2C_MT_SLA_NACK:
            I2cSendStart();
            break;
        case I2C_MT_SLA_ACK:
        case I2C_MT_DATA_ACK:
            if (i2c_index < i2c_len) {
                I2cSendByte(i2c_buf[i2c_index]);
	            i2c_index++;
            } 
            else {
	            I2cSendStop();
            }
            break;
        case I2C_MR_DATA_NACK:
            if (i2c_index < i2c_len) {
                i2c_buf[i2c_index] = I2C_DATA_REG;
            }
            I2cSendStop();
            break;
        default:
            I2cSendStop();
            /* LED_ON(2); FIXME log error */
    }
}

#endif  /* USE_I2C0 */

#if USE_I2C1

volatile uint8_t i2c1_status;
volatile uint8_t i2c1_buf[I2C1_BUF_LEN];
volatile uint8_t i2c1_len;
volatile uint8_t i2c1_index;
volatile uint8_t i2c1_slave_addr;
volatile bool_t* i2c1_finished;
extern volatile I2cStopCallback_t i2c1_stop_callback;

#define I2C1_DATA_REG   I2C1DAT
#define I2C1_STATUS_REG I2C1STAT

#define I2c1StopHandler() {}

#define I2c1SendAck()   { I2C1CONSET = _BV(AA); }
#define I2c1SendStop()  {						\
    I2C1CONSET = _BV(STO);						\
    if (i2c1_finished) *i2c1_finished = TRUE;				\
    i2c1_status = I2C_IDLE;						\
    if (i2c1_stop_callback)						\
		i2c1_stop_callback();					\
  }
#define I2c1SendStart() { I2C1CONSET = _BV(STA); }
#define I2c1SendByte(b) { I2C1_DATA_REG = b; }

#define I2c1Receive(_ack) {	    \
    if (_ack) I2C1CONSET = _BV(AA); \
    else I2C1CONCLR = _BV(AAC);	    \
  }

#define I2c1ClearStart() { I2C1CONCLR = _BV(STAC); }
#define I2c1ClearIT() { I2C1CONCLR = _BV(SIC); }

void i2c1_ISR(void) __attribute__((naked));
static inline void i2c1_automaton(uint32_t state);

void i2c1_ISR(void)
{
    ISR_ENTRY();

    uint32_t state = I2C1_STATUS_REG;

    i2c1_automaton(state);
    I2c1ClearIT();

    VICVectAddr = 0x00000000;             // clear this interrupt from the VIC
    ISR_EXIT();                           // recover registers and return
}

/* SDA1 on P0.14 */
/* SCL1 on P0.11 */
void i2c1_init(void) {
    /* set P0.11 and P0.14 to I2C1 */
    PINSEL0 |= 3 << 22 | 3 << 28;
    /* clear all flags */
    I2C1CONCLR = _BV(AAC) | _BV(SIC) | _BV(STAC) | _BV(I2ENC);
    /* enable I2C */
    I2C1CONSET = _BV(I2EN);
    /* set bitrate */
    I2C1SCLL = I2C1_SCLL_D;  
    I2C1SCLH = I2C1_SCLH_D;  

    // initialize the interrupt vector
    VICIntSelect &= ~VIC_BIT(VIC_I2C1);              // I2C0 selected as IRQ
    VICIntEnable = VIC_BIT(VIC_I2C1);                // I2C0 interrupt enabled
    _VIC_CNTL(I2C1_VIC_SLOT) = VIC_ENABLE | VIC_I2C1;
    _VIC_ADDR(I2C1_VIC_SLOT) = (uint32_t)i2c1_ISR;    // address of the ISR

    i2c1_status = I2C_IDLE;
    i2c1_finished = 0;
    i2c1_stop_callback = 0;
}


void i2c1_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished) {
    i2c1_len = len;
    i2c1_slave_addr = slave_addr | I2C_RECEIVE;
    i2c1_finished = finished;
    i2c1_status = I2C_BUSY;
    I2c1SendStart();
}

void i2c1_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished) {
    i2c1_len = len;
    i2c1_slave_addr = slave_addr & ~I2C_RECEIVE;
    i2c1_finished = finished;
    i2c1_status = I2C_BUSY;
    I2c1SendStart();
}

static inline void i2c1_automaton(uint32_t state)
{
    switch (state) {
        case I2C_START:
        case I2C_RESTART:
            I2c1SendByte(i2c1_slave_addr);
            I2c1ClearStart();
            i2c1_index = 0;
            break;
        case I2C_MR_DATA_ACK:
            if (i2c1_index < i2c1_len) {
                i2c1_buf[i2c1_index] = I2C1_DATA_REG;
                i2c1_index++;
                I2c1Receive(i2c1_index < i2c1_len - 1);
            }
            else {
                /* error , we should have got NACK */
                I2c1SendStop();
            }
            break;
        case I2C_MR_SLA_ACK: /* At least one char */
            /* Wait and reply with ACK or NACK */
            I2c1Receive(i2c1_index < i2c1_len - 1);
            break;
        case I2C_MR_SLA_NACK:
        case I2C_MT_SLA_NACK:
            I2c1SendStart();
            break;
        case I2C_MT_SLA_ACK:
        case I2C_MT_DATA_ACK:
            if (i2c1_index < i2c1_len) {
                I2c1SendByte(i2c1_buf[i2c1_index]);
                i2c1_index++;
            } else {
                I2c1SendStop();
            }
            break;
        case I2C_MR_DATA_NACK:
            if (i2c1_index < i2c1_len) {
                i2c1_buf[i2c1_index] = I2C1_DATA_REG;
            }
            I2c1SendStop();
            break;
        default:
            I2c1SendStop();
            /* LED_ON(2); FIXME log error */
    }
}
   
#endif /* USE_I2C1 */

