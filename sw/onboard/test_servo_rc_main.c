#include "std.h"

#include "config/config.h"
#include "config/airframe.h"

#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "rc.h"
#include "actuators.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

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
    hw_init();
    sys_time_init();
    led_init();
    actuators_init(ACTUATOR_BANK_SERVOS);
    rc_init();
    int_enable();
}

static inline void main_periodic_task( void ) {
    uint8_t i, val;

    rc_periodic_task();
    if (rc_status == RC_OK) {
        led_on(RC_LED);
        /* throttle values are in type pprz_t, it ranges from 0->9600
           so we need to scale this to 0->255 */
        val = (uint8_t)(((uint32_t)rc_values[RADIO_THROTTLE]*0xFF)/MAX_PPRZ);
    } else {
        led_off(RC_LED);
        val = 0;
    }

    for (i = 0; i < SERVOS_4017_NB_CHANNELS; i++) 
        actuators_set(ACTUATOR_BANK_SERVOS | i, val);

    actuators_commit(ACTUATOR_BANK_SERVOS);
}

static inline void main_event_task( void ) {
    rc_event_task();
}

