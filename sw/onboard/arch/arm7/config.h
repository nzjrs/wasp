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
#ifndef CONFIG_BOOZ2_V1_0_H
#define CONFIG_BOOZ2_V1_0_H

/* USB */
#define USE_USB_SERIAL 0

/* Master oscillator freq.       */
#define FOSC (12000000) 

/* PLL multiplier                */
#define PLL_MUL (5)         

/* CPU clock freq.               */
#define CCLK (FOSC * PLL_MUL) 

/* Peripheral bus speed mask 0x00->4, 0x01-> 1, 0x02 -> 2   */
#if USE_USB_SERIAL == 1
    #define PBSD_BITS 0x02    
    #define PBSD_VAL 2
#else
    #define PBSD_BITS 0x00    
    #define PBSD_VAL 4
#endif

/* Peripheral bus clock freq. */
#define PCLK (CCLK / PBSD_VAL) 

/* Onboard LEDs */
#define GPIO_1_BANK      1
#define GPIO_1_PIN       25
#define GPIO_2_BANK      1
#define GPIO_2_PIN       24
#define GPIO_3_BANK      1
#define GPIO_3_PIN       23
#define GPIO_4_BANK      1
#define GPIO_4_PIN       31

/* ADC */
/* battery: P0.29 AD0.2 */
#define ANALOG_BATT_PINSEL      PINSEL1
#define ANALOG_BATT_PINSEL_VAL  0x01
#define ANALOG_BATT_PINSEL_BIT  26

/* adc_spare: P0.13 AD1.4 */
#define ANALOG_SPARE_PINSEL     PINSEL0
#define ANALOG_SPARE_PINSEL_VAL 0x03
#define ANALOG_SPARE_PINSEL_BIT 26

/* pressure : P0.10 AD1.2 */
#define ANALOG_BARO_PINSEL      PINSEL0
#define ANALOG_BARO_PINSEL_VAL  0x03
#define ANALOG_BARO_PINSEL_BIT  20

/* use the onboard analog baro */
#define USE_ANALOG_BARO         1

/* Micromag on SSP, IMU connector */
#define MM_SS_PIN   28
#define MM_SS_IODIR IO1DIR
#define MM_SS_IOSET IO1SET
#define MM_SS_IOCLR IO1CLR

#define MM_RESET_PIN   19
#define MM_RESET_IODIR IO1DIR
#define MM_RESET_IOSET IO1SET
#define MM_RESET_IOCLR IO1CLR

#define MM_DRDY_PIN         30
#define MM_DRDY_PINSEL      PINSEL1
#define MM_DRDY_PINSEL_BIT  28
#define MM_DRDY_PINSEL_VAL  2
#define MM_DRDY_EINT        3
#define MM_DRDY_VIC_IT      VIC_EINT3

/* Servos: 4017 servo driver on CAM connector */
#define USE_SERVOS_4017         0
    #define SERVOS_4017_NB_CHANNELS 10

    #define SERVO_CLOCK_IODIR       IO0DIR
    #define SERVO_CLOCK_PIN         22          /* P0.22 aka MAT0.0  */
    #define SERVO_CLOCK_PINSEL      PINSEL1
    #define SERVO_CLOCK_PINSEL_VAL  0x03
    #define SERVO_CLOCK_PINSEL_BIT  12

    #define SERVO_RESET_PIN         21          /* P0.21 aka PWM5 */
    #define SERVO_RESET_IODIR       IO0DIR
    #define SERVO_RESET_IOSET       IO0SET
    #define SERVO_RESET_IOCLR       IO0CLR

/* Servos: Direct drive via PWM */
#define USE_SERVOS_DIRECT       1
    #define PWM_SERVO_0             1

/* Radio Control */
#define USE_RADIO_CONTROL       1

/* PPM : rc rx on P0.28 ( CAP0.2 ) */
#define PPM_PINSEL      PINSEL1
#define PPM_PINSEL_VAL  0x02
#define PPM_PINSEL_BIT  24

/* UARTS */
/* UART0 = uBlox GPS    */
/* UART1 = XBEE         */
#define USE_UART0 1
#define USE_UART1 1
#define UART0_BAUD B38400
#define UART1_BAUD B57600

/* I2C */
#define USE_I2C0 1      /* Motor Controllers */
#define USE_I2C1 0      /* AMI601 (Not used) */

#define I2C0_SCLL 150 
#define I2C0_SCLH 150

#define I2C1_SCLL 150
#define I2C1_SCLH 150

/* GPS */
#define GPS_LINK                    Uart0

/* VIC */
#define TIMER0_VIC_SLOT             1
#define UART0_VIC_SLOT              5
#define UART1_VIC_SLOT              6
#define USB_VIC_SLOT                7
#define MAX1168_EOC_VIC_SLOT        8
#define SSP_VIC_SLOT                9
#define I2C0_VIC_SLOT               10
/* #define I2C1_VIC_SLOT 11    AMI601 (Not used) */
#define MICROMAG_DRDY_VIC_SLOT      11

#endif /* CONFIG_BOOZ2_V1_0_H */
