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

#ifdef MESSAGE_ID_TEST_MESSAGE
    static uint8_t u8 = 1; static uint8_t i8 = -1; static uint16_t u16 = 10; static int16_t i16 = -10;
    static uint32_t u32 = 100; static int32_t i32 = -100; static float f = 0.0;
#endif

  comm_periodic_task(DA_COMM);

  RunOnceEvery(200, {
    led_toggle(4);

#ifdef MESSAGE_ID_TEST_MESSAGE
    MESSAGE_SEND_TEST_MESSAGE (DA_COMM, &u8, &i8, &u16, &i16, &u32, &i32, &f );
    u8 += 1; i8 -= 1; u16 += 10; i16 -= 10; u32 += 100; i32 -= 100; f += 15.0;
#endif

  })      

}

static inline void main_event_task( void ) {
  comm_event_task(DA_COMM);
}
