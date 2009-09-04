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
#define LED_1_BANK      1
#define LED_1_PIN       25
#define LED_2_BANK      1
#define LED_2_PIN       24
#define LED_3_BANK      1
#define LED_3_PIN       23
#define LED_4_BANK      1
#define LED_4_PIN       31

#define TIME_LED                1
#define RC_LED                  1
#define GPS_LED                 4
#define BOOZ2_ANALOG_BARO_LED   2
#define AHRS_ALIGNER_LED        3

/* PPM : rc rx on P0.28 ( CAP0.2 ) */
#define PPM_PINSEL      PINSEL1
#define PPM_PINSEL_VAL  0x02
#define PPM_PINSEL_BIT  24

/* ADC */

/* pressure : P0.10 AD1.2 */
#define ANALOG_BARO_PINSEL      PINSEL0
#define ANALOG_BARO_PINSEL_VAL  0x03
#define ANALOG_BARO_PINSEL_BIT  20
#define ANALOG_BARO_ADC         1

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

// damit, we have two of them now
//#define POWER_SWITCH_LED 3

/* Servos: 4017 servo driver on CAM connector */
#define USE_SERVOS_4017         1
#define SERVO_CLOCK_PIN         28          /* P0.28 aka MAT0.2  */
#define SERVO_CLOCK_PINSEL      PINSEL0
#define SERVO_CLOCK_PINSEL_VAL  0x02
#define SERVO_CLOCK_PINSEL_BIT  10
#define SERVO_DATA_PIN          23          /* p1.23 */
#define SERVO_RESET_PIN         24          /* p1.24 */

/* Time */
#define PERIODIC_TASK_PERIOD SYS_TICS_OF_SEC((1./512.))

/* Radio Control : Futaba is falling edge clocked whereas JR is rising edge */
#define RADIO_CONTROL       1
#define RC_FUTABA           0
#define RC_JR               1
#define RADIO_CONTROL_TYPE  RC_FUTABA

/* UARTS */
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
#define GPS_LINK Uart0

/* Analog */
#define BOOZ2_ANALOG_BARO_PERIOD SYS_TICS_OF_SEC((1./100.))
#define BOOZ2_ANALOG_BATTERY_PERIOD SYS_TICS_OF_SEC((1./10.))

/* Control Etc */
#define USE_VFF 1
#define DT_VFILTER (1./512.)
#define HS_YAW 1

#define BOOZ2_FMS_TYPE_NONE         0
#define BOOZ2_FMS_TYPE_DATALINK     1
#define BOOZ2_FMS_TYPE_TEST_SIGNAL  2
#define BOOZ2_FMS_TYPE              BOOZ2_FMS_TYPE_TEST_SIGNAL

/* VIC */
#define TIMER0_VIC_SLOT             1
#define ADC0_VIC_SLOT               2
#define ADC1_VIC_SLOT               3
#define UART0_VIC_SLOT              5
#define UART1_VIC_SLOT              6
#define USB_VIC_SLOT                7
#define MAX1168_EOC_VIC_SLOT        8
#define SSP_VIC_SLOT                9
#define I2C0_VIC_SLOT               10
/* #define I2C1_VIC_SLOT 11    AMI601 (Not used) */
#define MICROMAG_DRDY_VIC_SLOT      11

#endif /* CONFIG_BOOZ2_V1_0_H */
