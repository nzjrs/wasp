#ifndef RC_H
#define RC_H

#include "std.h"
#include "config.h"

#include "generated/radio.h"

typedef enum {
    RC_OK,
    RC_LOST,
    RC_REALLY_LOST
} RCStatus_t;

extern pprz_t       rc_values[RADIO_CTL_NB];
extern RCStatus_t   rc_status;

extern uint8_t  rc_values_contains_avg_channels;
extern uint8_t  time_since_last_ppm;
extern uint8_t  ppm_cpt, last_ppm_cpt;
extern uint16_t ppm_pulses[RADIO_CTL_NB];
extern bool_t   ppm_valid;

void
rc_init ( void );

void
rc_periodic_task ( void );

bool_t
rc_event_task ( void );

#endif /* RC_H */
