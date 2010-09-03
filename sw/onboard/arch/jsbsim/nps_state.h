#ifndef _NPS_STATE_H_
#define _NPS_STATE_H_

/* Copies the data from the sensors to the internal state of the autopilot */
void nps_state_update(void);

void nps_state_init(bool_t bypass_ahrs);

#endif /* _NPS_STATE_H_ */
