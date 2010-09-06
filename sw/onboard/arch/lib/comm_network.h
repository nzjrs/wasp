#ifndef _COMM_NETWORK_H_
#define _COMM_NETWORK_H_

#include "std.h"
#include <glib.h>

void    comm_network_init ( const gchar *host, guint16 port );
void    comm_network_start_message_hw ( void );
void    comm_network_end_message_hw ( void );
bool_t  comm_network_ch_available ( void );
void    comm_network_send_ch ( uint8_t c );
uint8_t comm_network_get_ch( void );

#endif /* _COMM_NETWORK_H_ */

