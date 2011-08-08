#include "std.h"
#include "arm7/config.h"
#include "arm7/servos_direct_hw.h"

uint8_t         servos_direct_last_value;
const uint8_t   servos_direct_pwm_latch_value = 0
#if defined PWM_SERVO_0
    | PWM_SERVO_0_LATCH 
#endif
#if defined PWM_SERVO_1
    | PWM_SERVO_1_LATCH 
#endif
#if defined PWM_SERVO_2
    | PWM_SERVO_2_LATCH 
#endif
#if defined PWM_SERVO_3
    | PWM_SERVO_3_LATCH 
#endif
#if defined PWM_SERVO_4
    | PWM_SERVO_4_LATCH 
#endif
#if defined PWM_SERVO_5
    | PWM_SERVO_5_LATCH 
#endif
  ;

void servos_direct_init(void)
{
  /* configure pins for PWM */
#if defined PWM_SERVO_0
  PWM_SERVO_0_PINSEL = (PWM_SERVO_0_PINSEL & PWM_SERVO_0_PINSEL_MASK) | PWM_SERVO_0_PINSEL_VAL << PWM_SERVO_0_PINSEL_BIT;
#endif
#if defined PWM_SERVO_1
  PWM_SERVO_1_PINSEL = (PWM_SERVO_1_PINSEL & PWM_SERVO_1_PINSEL_MASK) | PWM_SERVO_1_PINSEL_VAL << PWM_SERVO_1_PINSEL_BIT;
#endif
#if defined PWM_SERVO_2
  PWM_SERVO_2_PINSEL = (PWM_SERVO_2_PINSEL & PWM_SERVO_2_PINSEL_MASK) | PWM_SERVO_2_PINSEL_VAL << PWM_SERVO_2_PINSEL_BIT;
#endif
#if defined PWM_SERVO_3
  PWM_SERVO_3_PINSEL = (PWM_SERVO_3_PINSEL & PWM_SERVO_3_PINSEL_MASK) | PWM_SERVO_3_PINSEL_VAL << PWM_SERVO_3_PINSEL_BIT;
#endif
#if defined PWM_SERVO_4
  PWM_SERVO_4_PINSEL = (PWM_SERVO_4_PINSEL & PWM_SERVO_4_PINSEL_MASK) | PWM_SERVO_4_PINSEL_VAL << PWM_SERVO_4_PINSEL_BIT;
#endif
#if defined PWM_SERVO_5
  PWM_SERVO_5_PINSEL = (PWM_SERVO_5_PINSEL & PWM_SERVO_5_PINSEL_MASK) | PWM_SERVO_5_PINSEL_VAL << PWM_SERVO_5_PINSEL_BIT;
#endif

  /* set servo refresh rate */
  PWMMR0 = SERVOS_TICS_OF_USEC(10000);

  /* FIXME: For now, this prescaler needs to match the TIMER0 prescaler, as the
  higher level code treats them the same */
  PWMPR = 1;

  /* enable all 6 PWM outputs in single edge mode*/
  PWMPCR = 0
#if defined PWM_SERVO_0
    | PWM_SERVO_0_ENA 
#endif
#if defined PWM_SERVO_1
    | PWM_SERVO_1_ENA 
#endif
#if defined PWM_SERVO_2
    | PWM_SERVO_2_ENA 
#endif
#if defined PWM_SERVO_3
    | PWM_SERVO_3_ENA 
#endif
#if defined PWM_SERVO_4
    | PWM_SERVO_4_ENA 
#endif
#if defined PWM_SERVO_5
    | PWM_SERVO_5_ENA 
#endif
    ;

  /* commit PWMMRx changes */
  PWMLER = PWMLER_LATCH0;

  /* enable PWM timer in PWM mode */
  PWMTCR = PWMTCR_COUNTER_ENABLE | PWMTCR_PWM_ENABLE;

  PWMLER = servos_direct_pwm_latch_value;
}

/* only one channel supported at once... */
uint8_t servos_direct_get_num(void)
{
    return 1;
}

void servos_direct_set(uint8_t id, uint8_t value)
{
    uint16_t tval;

    servos_direct_last_value = value;

    uint16_t tmp = ((((uint32_t)value*650)/0xFF) + 500);
    tval = SERVOS_TICS_OF_USEC(tmp);


#if defined PWM_SERVO_0
    SERVO_REG_0 = tval;
#endif
#if defined PWM_SERVO_1
    SERVO_REG_1 = tval;
#endif
#if defined PWM_SERVO_2
    SERVO_REG_2 = tval;
#endif
#if defined PWM_SERVO_3
    SERVO_REG_3 = tval;
#endif
#if defined PWM_SERVO_4
    SERVO_REG_4 = tval;
#endif
#if defined PWM_SERVO_5
    SERVO_REG_5 = tval;
#endif

}

uint8_t servos_direct_get(uint8_t id)
{
    return servos_direct_last_value;
}

void servos_direct_commit(void)
{
    PWMLER = servos_direct_pwm_latch_value;
}

