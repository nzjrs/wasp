#include "std.h"
#include "config/config.h"

#include "comm.h"
#include "arm7/comm_hw.h"
#include "arm7/uart_hw.h"
#include "arm7/usb_ser_hw.h"
#include "arm7/led_hw.h"

SystemStatus_t comm_system_status = STATUS_UNINITIAIZED;

void
comm_init ( CommChannel_t chan )
{
#if USE_UART0
    if ( chan == COMM_0 ) {
        uart0_init_tx();
        comm_channel_used[chan] = TRUE;
    }
#endif
#if USE_UART1
    if ( chan == COMM_1 ) {
        uart1_init_tx();
        comm_channel_used[chan] = TRUE;
    }
#endif
#if USE_USB_SERIAL
    if ( chan == COMM_USB ) {
        VCOM_init();
        comm_channel_used[chan] = TRUE;
    }
#endif

    for (uint8_t i = 0; i < COMM_NB; i++) {
        comm_callback_rx[i] = 0;
        comm_callback_tx[i] = 0;
    
        comm_status[i].parse_state = STATE_UNINIT;
        comm_status[i].msg_received = FALSE;
        comm_status[i].buffer_overrun = 0;
        comm_status[i].parse_error = 0;
    }

    comm_system_status = STATUS_INITIALIZED;
}

bool_t
comm_ch_available ( CommChannel_t chan )
{
#if USE_UART0
    if (chan == COMM_0) {
        return Uart0ChAvailable();
    }
#endif
#if USE_UART1
    if (chan == COMM_1) {
        return Uart1ChAvailable();
    }
#endif
#if USE_USB_SERIAL
    if (chan == COMM_USB)
        return VCOM_check_available();
#endif
    return FALSE;
}

uint8_t
comm_get_ch( CommChannel_t chan )
{
    comm_system_status = STATUS_ALIVE;

#if USE_UART0
    if (chan == COMM_0) {
        return Uart0Getch();
    }
#endif
#if USE_UART1
    if (chan == COMM_1) {
        return Uart1Getch();
    }
#endif
#if USE_USB_SERIAL
    if (chan == COMM_USB)
        return VCOM_getchar();
#endif
    return '\0';
}

void
comm_send_ch( CommChannel_t chan, uint8_t ch )
{
    comm_system_status = STATUS_ALIVE;

#if USE_UART0
    if (chan == COMM_0)
        uart0_transmit(ch);
#endif
#if USE_UART1
    if (chan == COMM_1)
        uart1_transmit(ch);
#endif
#if USE_USB_SERIAL
    if (chan == COMM_USB)
        VCOM_putchar(ch);
#endif
}

bool_t
comm_check_free_space ( CommChannel_t chan, uint8_t len )
{
#if USE_UART0
    if (chan == COMM_0)
        return uart0_check_free_space(len);
#endif
#if USE_UART1
    if (chan == COMM_1)
        return uart1_check_free_space(len);
#endif
#if USE_USB_SERIAL
    if (chan == COMM_USB)
        return VCOM_check_free_space(len);
#endif
    return FALSE;
}

void
comm_overrun ( CommChannel_t chan )
{
    if (chan < COMM_NB)
        comm_status[chan].buffer_overrun++;
}

