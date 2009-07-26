#ifndef COMM_AUTOPILOT_H
#define COMM_AUTOPILOT_H

#include "comm.h"

bool_t
comm_autopilot_send ( CommChannel_t chan, uint8_t msgid );

bool_t 
comm_autopilot_message_received (CommChannel_t chan, CommMessage_t *message);

#endif /* COMM_AUTOPILOT_H */
