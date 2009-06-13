#include "std.h"
#include "config.h"

#include "comm.h"
#include "arm7/comm_hw.h"
#include "arm7/uart_hw.h"
#include "arm7/usb_ser_hw.h"
#include "arm7/led_hw.h"

void
comm_init ( CommChannel_t chan )
{
    if ( chan == COMM_1 ) {
        uart1_init_tx();
        comm_channel_used[chan] = TRUE;
    }
#if USE_USB_SERIAL
    else if ( chan == COMM_2 ) {
        VCOM_init();
        comm_channel_used[chan] = TRUE;
    }
#endif

    for (uint8_t i = 0; i < COMM_NB; i++) {
        comm_callback[i] = 0;
    
        comm_status[i].parse_state = STATE_UNINIT;
        comm_status[i].payload_idx = 0;
        comm_status[i].pprz_msg_received = FALSE;
        comm_status[i].pprz_ovrn = 0;
        comm_status[i].pprz_error = 0;
    }

}

bool_t
comm_ch_available ( CommChannel_t chan )
{
    if (chan == COMM_1) {
        return Uart1ChAvailable();
    }
#if USE_USB_SERIAL
    else if (chan == COMM_2)
        return VCOM_check_available();
#endif
    else
        return FALSE;
}

uint8_t
comm_get_ch( CommChannel_t chan )
{
    if (chan == COMM_1) {
        return Uart1Getch();
    }
#if USE_USB_SERIAL
    else if (chan == COMM_2)
        return VCOM_getchar();
#endif
    else return '\0';
}

void
comm_send_ch( CommChannel_t chan, uint8_t ch )
{
    if (chan == COMM_1)
        uart1_transmit(ch);
#if USE_USB_SERIAL
    else if (chan == COMM_2)
        VCOM_putchar(ch);
#endif
}

bool_t
comm_check_free_space ( CommChannel_t chan, uint8_t len )
{
    if (chan == COMM_1)
        return uart1_check_free_space(len);
#if USE_USB_SERIAL
    else if (chan == COMM_2)
        return VCOM_check_free_space(len);
#endif
    else
        return FALSE;
}
