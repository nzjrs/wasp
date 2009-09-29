#ifndef ALTIMETER_H
#define ALTIMETER_H

#include "std.h"

extern SystemStatus_t altimeter_system_status;

extern uint16_t booz2_analog_baro_offset;
extern uint16_t booz2_analog_baro_value;
extern uint16_t booz2_analog_baro_value_filtered;
extern bool_t   booz2_analog_baro_data_available;

void
altimeter_init(void);

void
altimeter_periodic_task(void);

uint8_t 
altimeter_event_task ( void );

int32_t
altimeter_get_altitude( void );

#endif /* ALTIMETER_H */
