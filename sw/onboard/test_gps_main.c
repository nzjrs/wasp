#include "std.h"
#include "init_hw.h"
#include "sys_time.h"
#include "led.h"
#include "interrupt_hw.h"
#include "comm.h"
#include "gps.h"

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

static inline void main_init( void ) {
  hw_init();
  sys_time_init();
  led_init();

  /* Uart 1 */
  comm_init(COMM_1);

  gps_init();

  int_enable();
}

static inline void main_periodic_task( void ) {

  RunOnceEvery(250, {
    comm_send_ch(COMM_1, booz_gps_state.num_sv);
  });


}

static inline void main_event_task( void ) {
  if (gps_event_task())
    if (booz_gps_state.fix == GPS_FIX_3D)
        led_on(GPS_LED);
}

