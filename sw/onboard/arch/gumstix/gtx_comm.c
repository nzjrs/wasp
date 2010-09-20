#include "std.h"
#include "comm.h"

#include "lib/comm_network.h"

SystemStatus_t comm_system_status = STATUS_UNINITIAIZED;

void comm_init ( CommChannel_t chan )
{
    uint8_t i;

    comm_channel_used[chan] = TRUE;
    comm_system_status = STATUS_INITIALIZED;

    for (i = 0; i < COMM_NB; i++) {
        comm_callback_rx[i] = 0;
        comm_callback_tx[i] = 0;

        comm_status[i].parse_state = STATE_UNINIT;
        comm_status[i].msg_received = FALSE;
        comm_status[i].buffer_overrun = 0;
        comm_status[i].parse_error = 0;
    }

    comm_network_init ("192.168.0.1", 1212);
}

bool_t comm_ch_available ( CommChannel_t chan )
{
    return comm_network_ch_available();
}

void comm_send_ch ( CommChannel_t chan, uint8_t c )
{
    comm_network_send_ch (c);
}

uint8_t comm_get_ch( CommChannel_t chan )
{
    return comm_network_get_ch ();
}

void comm_start_message_hw ( CommChannel_t chan )
{
    comm_network_start_message_hw ();
}

void comm_end_message_hw ( CommChannel_t chan )
{
    comm_network_end_message_hw ();
}

bool_t  comm_check_free_space ( CommChannel_t chan, uint8_t len ) { return TRUE; }
void    comm_overrun ( CommChannel_t chan ) {}

