#ifndef _COMM_FIFO_H_
#define _COMM_FIFO_H_

#include "std.h"

bool_t  comm_fifo_init ( void );
bool_t  comm_fifo_ch_available ( void );
void    comm_fifo_send_ch ( uint8_t c);
uint8_t comm_fifo_get_ch( void );

#endif /* _COMM_FIFO_H_ */
