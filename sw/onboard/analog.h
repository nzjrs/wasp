#ifndef ANALOG_H
#define ANALOG_H

#include "std.h"

typedef enum {
    ANALOG_CHANNEL_1,
    ANALOG_CHANNEL_2,
    ANALOG_CHANNEL_3,
    ANALOG_CHANNEL_4,
    ANALOG_CHANNEL_5,
    ANALOG_CHANNEL_6,
    ANALOG_CHANNEL_7,
    ANALOG_CHANNEL_8
} AnalogChannel_t;

void 
analog_init( void );

uint16_t
analog_read_channel( AnalogChannel_t channel );

uint8_t
analog_read_battery( void );

#endif /* ANALOG_H */
