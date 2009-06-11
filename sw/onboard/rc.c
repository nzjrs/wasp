#include "rc.h"

pprz_t  rc_values[RADIO_CTL_NB];
uint8_t rc_status;
int32_t avg_rc_values[RADIO_CTL_NB];
uint8_t rc_values_contains_avg_channels = FALSE;

uint8_t time_since_last_ppm;
uint8_t ppm_cpt, last_ppm_cpt;
uint16_t ppm_pulses[RADIO_CTL_NB];
bool_t ppm_valid;

//FIXME: When the downlink has been abstracted
//
//void
//rc_downlink_send_ppm ( void ) {
//    downlink_send_
//}
//void
//rc_downlink_send_rc ( void ) {
//    downlink_send_
//}
