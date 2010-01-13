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

#include "config/config.h"
#include "generated/settings.h"

#include "LPC21xx.h"
#include "arm7/armVIC.h"

#include "sys_time.h"
#include "arm7/sys_time_hw.h"
#include "arm7/led_hw.h"

#include "arm7/rc_hw.h"             /* ppm_isr */
#include "arm7/servos_4017_hw.h"    /* servos_4017_isr */

uint8_t  cpu_usage;
uint16_t cpu_time_sec;
uint32_t cpu_time_ticks;
uint32_t last_periodic_event;

uint32_t chrono_start; /* T0TC ticks */

#define TIMER0_IT_MASK (TIR_CR2I | TIR_MR0I)

void TIMER0_ISR ( void ) __attribute__((naked));
void TIMER0_ISR ( void ) {
  ISR_ENTRY();

  while (T0IR & TIMER0_IT_MASK) {
#ifdef USE_RADIO_CONTROL
    if (T0IR&TIR_CR2I) {
      ppm_isr();
      /* clear interrupt */
      T0IR = TIR_CR2I;
    }
#endif
#if USE_SERVOS_4017
    if (T0IR&TIR_MR0I) {
        servos_4017_isr();
        /* clear interrupt */
        T0IR = TIR_MR0I;
    }
#endif
  }
  VICVectAddr = 0x00000000;

  ISR_EXIT();
}

void sys_time_init( void ) {
  /* setup Timer 0 to count forever  */
  /* reset & disable timer 0         */
  T0TCR = TCR_RESET;
  /* set the prescale divider        */
  T0PR = T0_PCLK_DIV - 1;
  /* disable match registers         */
  T0MCR = 0;
  /* disable compare registers       */
  T0CCR = 0;
  /* disable external match register */
  T0EMR = 0;                          
  /* enable timer 0                  */
  T0TCR = TCR_ENABLE;

  cpu_time_sec = 0;
  cpu_time_ticks = 0;
  last_periodic_event = 0;

  /* select TIMER0 as IRQ    */
  VICIntSelect &= ~VIC_BIT(VIC_TIMER0);
  /* enable TIMER0 interrupt */
  VICIntEnable = VIC_BIT(VIC_TIMER0); 
  /* on slot vic slot 1      */
  _VIC_CNTL(TIMER0_VIC_SLOT) = VIC_ENABLE | VIC_TIMER0;
  /* address of the ISR      */
  _VIC_ADDR(TIMER0_VIC_SLOT) = (uint32_t)TIMER0_ISR; 

}

bool_t sys_time_periodic( void ) {
  uint32_t now = T0TC;
  uint32_t dif = now - last_periodic_event;
  if ( dif >= PERIODIC_TASK_PERIOD) {
    last_periodic_event += PERIODIC_TASK_PERIOD;
    cpu_time_ticks += PERIODIC_TASK_PERIOD;
    if (cpu_time_ticks > TIME_TICKS_PER_SEC) {
      cpu_time_ticks -= TIME_TICKS_PER_SEC;
      cpu_time_sec++;
#ifdef LED_TIME
      LED_TOGGLE(LED_TIME)
#endif
    }
    return TRUE;
  }
  return FALSE;
}

void sys_time_chrono_start ( void ) {
  chrono_start = T0TC;
}

uint32_t sys_time_chrono_stop ( void ) {
  return T0TC - chrono_start;
}

void sys_time_usleep(uint32_t us) {
  uint32_t start = T0TC;
  uint32_t ticks = SYS_TICS_OF_USEC(us);
  while ((uint32_t)(T0TC-start) < ticks);
}

void sys_time_calculate_cpu_usage ( void ) {
  uint32_t now = T0TC;
  uint32_t dif = now - last_periodic_event;
  cpu_usage = (dif*100)/PERIODIC_TASK_PERIOD;
}
