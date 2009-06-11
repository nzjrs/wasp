#include <inttypes.h>

#include "std.h"
#include "init_hw.h"
#include "sys_time.h"
#include "led.h"
#include "interrupt_hw.h"
#include "comm.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

#define DA_COMM COMM_1

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

  comm_init(DA_COMM);

  int_enable();
}

static inline void main_periodic_task( void ) {
  
  RunOnceEvery(200, {
    led_toggle(4);
    comm_periodic_task(DA_COMM);
  });

}

static inline void main_event_task( void ) {
    comm_event_task(DA_COMM);
}
