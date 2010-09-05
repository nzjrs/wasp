#include <glib.h>
#include <gio/gio.h>

#include "std.h"
#include "comm.h"

#include "generated/messages.h"
#include "generated/settings.h"

GSocket *socket = NULL;

void comm_network_init ( CommChannel_t chan )
{
    socket = g_socket_new(G_SOCKET_FAMILY_IPV4,
                          G_SOCKET_TYPE_DATAGRAM,
                          G_SOCKET_PROTOCOL_UDP,
                          NULL);
}




