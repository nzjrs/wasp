#include <glib.h>
#include <gio/gio.h>

#include "std.h"
#include "comm.h"
#include "messages_types.h"

#include "generated/messages.h"
#include "generated/settings.h"

#include "lib/comm_network.h"

/*
http://beej.us/guide/bgnet/output/html/multipage/clientserver.html#datagram
*/

GSocketAddress  *address = NULL;
GSocket         *socket = NULL;

#define BUF_LEN (COMM_MAX_PAYLOAD_LEN + COMM_NUM_NON_PAYLOAD_BYTES)
uint8_t         tx_buf[BUF_LEN];
uint8_t         rx_buf[BUF_LEN];
int             tx_i;
int             rx_i;
int             rx_len;

void comm_network_init ( const gchar *host, guint16 port )
{
    GInetAddress *hostaddress, *localaddress;
    GSocketAddress *local;

    tx_i = 0;
    rx_i = 0;
    rx_len = 0;

    socket = g_socket_new(G_SOCKET_FAMILY_IPV4,
                          G_SOCKET_TYPE_DATAGRAM,
                          G_SOCKET_PROTOCOL_UDP,
                          NULL);

    hostaddress = g_inet_address_new_from_string(host);
    address = g_inet_socket_address_new(hostaddress, port);
    g_object_unref(hostaddress);

    /* bind to local address to start receiving connections */
    localaddress = g_inet_address_new_from_string("127.0.0.1");
    local = g_inet_socket_address_new(localaddress, port);
    g_object_unref(localaddress);
    g_socket_bind(socket,
                  local,
                  TRUE,
                  NULL);

    g_socket_set_blocking (socket, FALSE);
}

void comm_network_start_message_hw ( void )
{
    tx_i = 0;
}

void comm_network_end_message_hw ( void )
{
    GError *err = NULL;

    gssize sent = g_socket_send_to(socket,
                                   address,
                                   (const gchar *)tx_buf,
                                   tx_i,
                                   NULL,
                                   &err);
    if (sent != tx_i)
        ;
}

bool_t comm_network_ch_available ( void )
{
    GError *err = NULL;

    /* Bail if we are still processing the last packet */
    if (rx_len && rx_i != (rx_len - 1))
        return TRUE;

    gssize got = g_socket_receive(socket,
                                  (gchar *)rx_buf,
                                  BUF_LEN,
                                  NULL,
                                  &err);

    if (got != -1) {
        rx_len = got;
        rx_i = 0;
        return TRUE;
    }

    return FALSE;
}

void comm_network_send_ch ( uint8_t c )
{
    tx_buf[tx_i++] = c;
}

uint8_t comm_network_get_ch( void )
{
    return rx_buf[rx_i++];
}


