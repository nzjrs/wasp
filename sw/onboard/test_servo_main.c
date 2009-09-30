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

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

uint32_t t0, t1, diff;

int main( void ) {
    main_init();
    while(1) {
        if (sys_time_periodic())
            main_periodic_task();
        main_event_task();
    }
    return 0;
}

static inline void main_init( void ) {
    hw_init();
    sys_time_init();
    led_init();
    actuators_init(ACTUATOR_BANK_SERVOS);
    int_enable();
}

#define SERVO_SEPERATION    (0xFF/SERVOS_4017_NB_CHANNELS)
#define SERVO_MIN           0x00
#define SERVO_MAX           0xFF
#define SERVO_SPEED         0

static inline void main_periodic_task( void ) {
    static uint8_t  val = 0;
    static uint16_t cnt = 0;

    if (++cnt == 200) 
    {
        uint8_t i,j;

        /* Evenly space all servo values through the full range */
        for (i = 0, j = 0; i < SERVOS_4017_NB_CHANNELS; i++, j += SERVO_SEPERATION)
            actuators_set(
                ACTUATOR_BANK_SERVOS | i,
                Chop(val + j, SERVO_MIN, SERVO_MAX)
            );

        actuators_commit(ACTUATOR_BANK_SERVOS);
        val += SERVO_SPEED;
        cnt = 0;
    }
}

static inline void main_event_task( void ) {

}

