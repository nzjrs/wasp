#ifndef ANALOG_H
#define ANALOG_H

#include "std.h"

typedef enum {
    ANALOG_CHANNEL_BATTERY = 0,
    ANALOG_CHANNEL_PRESSURE,
    ANALOG_CHANNEL_ADC_SPARE,
    ANALOG_CHANNEL_4,
    ANALOG_CHANNEL_5,
    ANALOG_CHANNEL_6,
    ANALOG_CHANNEL_7,
    ANALOG_CHANNEL_8,
    ANALOG_CHANNEL_NUM
} AnalogChannel_t;

void 
analog_init(void);

void
analog_enable_channel( AnalogChannel_t channel );

/* returns the raw ADC value for the requested channel */
uint16_t
analog_read_channel( AnalogChannel_t channel );

/* returns the battery voltage, in decivolts */
uint8_t
analog_read_battery( void );

bool_t analog_event_task( void );

void analog_periodic_task( void );

#endif /* ANALOG_H */
