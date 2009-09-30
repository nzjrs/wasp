#ifndef SYS_TIME_H
#define SYS_TIME_H

#include "std.h"

/* the number of seconds the CPU has been running */
extern uint16_t cpu_time_sec;

/* the estimated CPU usages, percent, 0-100 */
extern uint8_t  cpu_usage;

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

/**
 * Calculates an approximation of the CPU usage, assuming
 * this function is called immediately before 
 * sys_time_get_periodic.
 */
void sys_time_calculate_cpu_usage ( void );

#endif /* SYS_TIME_H */
