#include <inttypes.h>

#include "std.h"
#include "init_hw.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "rc.h"

#include "interrupt_hw.h"


static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

int main( void ) {
    main_init();
    while(1)
    {
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

    rc_init();

    int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(COMM_1);

    rc_periodic_task();
    if (rc_status == RC_OK)
        led_on(RC_LED);
    else
        led_off(RC_LED);

    RunOnceEvery(250, {
        MESSAGE_SEND_PPM(COMM_1, ppm_pulses);
        MESSAGE_SEND_RC(COMM_1, rc_values);
    });

}

static inline void main_event_task( void )
{
    comm_event_task(COMM_1);
    rc_event_task();
}

