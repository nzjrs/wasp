#include <stdio.h>
#include <stdlib.h>

#include "wasp.h"

void comm_send_ch ( CommChannel_t chan, uint8_t c )
{
    printf("\t0x%X\n", c);
}

int main ( void )
{
    comm_init(0xFD);

    printf("Sending message: %s\n", message_get_name(MESSAGE_ID_TIME));
    message_send_time (COMM_0, 30);

    printf("Sending message: %s\n", message_get_name(MESSAGE_ID_MOTORS_STOP));
    message_send_motors_stop (COMM_0);

    return 0;
}
