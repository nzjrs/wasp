#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "analog.h"
#include "altimeter.h"

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

    analog_init();
    altimeter_init();

    int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(COMM_1);
    RunOnceEvery(250, {
        int32_t alt = altimeter_get_altitude();
        MESSAGE_SEND_ALTIMETER(COMM_1,
            &alt,
            &altimeter_system_status,
            &booz2_analog_baro_offset,
            &booz2_analog_baro_value);
    });
}

static inline void main_event_task( void )
{
    altimeter_event_task();
    comm_event_task(COMM_1);
}

