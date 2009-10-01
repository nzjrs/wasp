#include "std.h"

#include "config/config.h"
#include "config/airframe.h"

#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "rc.h"

#include "generated/messages.h"
#include "comm.h"

#include "actuators.h"

typedef struct {
    uint8_t val;
    uint8_t dval;
} Servo_t;

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

uint32_t t0, t1, diff;
Servo_t servos[SERVOS_4017_NB_CHANNELS];

int main( void ) {
    main_init();
    while(1) {
        if (sys_time_periodic())
            main_periodic_task();
        main_event_task();
    }
    return 0;
}

#define SERVO_SEPERATION    (0xFF/SERVOS_4017_NB_CHANNELS)

static inline void main_init( void ) {
    uint8_t i,j;

    hw_init();
    sys_time_init();
    led_init();
    actuators_init(ACTUATOR_BANK_SERVOS);
    int_enable();

    /* Initialise all servos to values which are
       evenly spaced through the full range */
    for (i = 0, j = 0; i < SERVOS_4017_NB_CHANNELS; i++, j += SERVO_SEPERATION) {
        servos[i].val = j;
        /* starting moving in the forward direction */
        servos[i].dval = 1;
    }
        

}


#define SERVO_MIN           0x00
#define SERVO_MAX           0xFF
#define SERVO_SPEED         5

/* define as non zero to set all servos to this value */
//#define SERVO_FIXED_VALUE   (0xFF/2)

static inline void main_periodic_task( void ) {
    uint8_t i;
    static uint16_t cnt = 0;

    if (++cnt == SERVO_SPEED) 
    {
        /* Move all servos forward or backward by dval */
        for (i = 0; i < SERVOS_4017_NB_CHANNELS; i++) 
        {
            Servo_t *servo = &servos[i];

            /* reverse servos when they get to the end */
            if (servo->val == SERVO_MAX && servo->dval == 1)
                servo->dval = -1;
            else if (servo->val == SERVO_MIN)
                servo->dval = 1;

            /* move and set servo */
            servo->val += servo->dval;
#if SERVO_FIXED_VALUE > 0
            actuators_set(ACTUATOR_BANK_SERVOS | i, SERVO_FIXED_VALUE);
#else
            actuators_set(ACTUATOR_BANK_SERVOS | i, servo->val);
#endif
        }

        actuators_commit(ACTUATOR_BANK_SERVOS);
        cnt = 0;
    }
}

static inline void main_event_task( void ) {

}

