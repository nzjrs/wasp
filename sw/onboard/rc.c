#include "rc.h"

pprz_t          rc_values[RADIO_CTL_NB];
RCStatus_t      rc_status;

uint8_t rc_values_contains_avg_channels = FALSE;
uint8_t time_since_last_ppm;
uint8_t ppm_cpt, last_ppm_cpt;
uint16_t ppm_pulses[RADIO_CTL_NB];


