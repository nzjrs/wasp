#include "std.h"

#include "config/config.h"
#include "config/airframe.h"

#include "init.h"
#include "sys_time.h"
#include "led.h"

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

    comm_init(COMM_1);

    actuators_init();

    int_enable();
}

static inline void main_periodic_task( void ) {
    static uint16_t i = 0;

    switch(i++) 
    {
        case 1:
            actuators_set(SERVO_FRONT, 0);
            actuators_set(SERVO_BACK, 0);
            actuators_set(SERVO_RIGHT, 0);
            actuators_set(SERVO_LEFT, 0);
            break;
        case 2001:
            actuators_set(SERVO_FRONT, 15);
            break;
        case 4001:
            actuators_set(SERVO_BACK, 15);
            break;
        case 6001:
            actuators_set(SERVO_RIGHT, 15);
            break;
        case 8001:
            actuators_set(SERVO_LEFT, 15);
            break;
        case 10001:
            i = 0;
            break;
    }
    actuators_commit();
}

static inline void main_event_task( void ) {

}

