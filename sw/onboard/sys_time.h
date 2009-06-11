#ifndef SYS_TIME_H
#define SYS_TIME_H

#include "std.h"

/* interface to be implemented by hardware */

extern uint16_t cpu_time_sec;

void
sys_time_init( void );

bool_t 
sys_time_periodic( void );

void
sys_time_chrono_start ( void );

uint32_t 
sys_time_chrono_stop ( void );

void
sys_time_usleep ( uint32_t us );

#endif /* SYS_TIME_H */
