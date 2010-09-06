#include "std.h"
#include "comm.h"

#include "lib/comm_network.h"

SystemStatus_t comm_system_status = STATUS_UNINITIAIZED;

void comm_init ( CommChannel_t chan )
{
    comm_network_init ("192.168.1.3", 1212);
}

bool_t comm_ch_available ( CommChannel_t chan ) { return FALSE; }

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

