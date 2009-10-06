//based on LED test main

#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"

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
  int_enable();
}

static inline void main_periodic_task( void ) {
  //turn Leds 2-4 on and off periodically
  static int tick=2, increment=1;
  RunOnceEvery(100, {
    led_toggle(tick);
    tick += increment;
    if (tick > 4 || tick < 2) increment*=-1;
  });
}

static inline void main_event_task( void ) {

}
