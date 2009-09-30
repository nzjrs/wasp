#ifndef SERVOS_4017_HW_H
#define SERVOS_4017_HW_H

#include "std.h"
#include "LPC21xx.h"
#include "config/config.h"
#include "arm7/led_hw.h"
#include "arm7/sys_time_hw.h"

#define SERVOS_4017_NB_CHANNELS         10
#define SERVOS_TICS_OF_USEC(s)          SYS_TICS_OF_USEC(s)
#define SERVOS_4017_RESET_WIDTH         SERVOS_TICS_OF_USEC(1000)
#define SERVOS_4017_FIRST_PULSE_WIDTH   SERVOS_TICS_OF_USEC(100)

extern uint16_t servos_values[SERVOS_4017_NB_CHANNELS];
extern uint8_t servos_4017_idx;

void servos_4017_init(void);

static inline void servos_4017_isr(void)
{
    LED_ON(2);

    if (servos_4017_idx == SERVOS_4017_NB_CHANNELS) 
    {
        SetBit(SERVO_RESET_IOSET, SERVO_RESET_PIN);
        /* Start a long 1ms reset, keep clock low */
        T0MR0 += SERVOS_4017_RESET_WIDTH;
        servos_4017_idx++;
        T0EMR &= ~TEMR_EM0;
    }
    else if (servos_4017_idx > SERVOS_4017_NB_CHANNELS) 
    {
        /* Clear the reset*/
        SetBit(SERVO_RESET_IOCLR, SERVO_RESET_PIN);
        /* assert clock */
        T0EMR |= TEMR_EM0;
        /* Starts a short pulse-like period */
        T0MR0 += SERVOS_4017_FIRST_PULSE_WIDTH;
        servos_4017_idx=0; /* Starts a new sequence next time */
    }
    else 
    {
        /* request next match */
        T0MR0 += servos_values[servos_4017_idx];
        /* clock low if not last one, last is done with reset */
        if (servos_4017_idx != SERVOS_4017_NB_CHANNELS-1) 
        {
            /* raise clock pin */
            T0EMR |= TEMR_EM0;
        }
        servos_4017_idx++;
    }
}

#endif /* SERVOS_4017_HW_H */
