#include <glib.h>
#include <glib-object.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"

#include "lib/time_helpers.h"

uint16_t cpu_time_sec;
uint8_t  cpu_usage;

void hw_init(void)
{
    g_thread_init(NULL);
    g_type_init();
}

void sys_time_init( void )
{
    cpu_usage = 0;
    cpu_time_sec = 0;

    time_helpers_init();
}

bool_t sys_time_periodic( void )
{
    gdouble cpu_time;
    gulong sleep_time;
    bool_t should_run;

    cpu_time = time_helpers_check_periodic(&should_run, &cpu_usage, &sleep_time);
    cpu_time_sec = cpu_time;


    if (should_run == FALSE)
        time_helpers_sleep(sleep_time);
        
    return should_run;
}

void    sys_time_calculate_cpu_usage ( void ) {}

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


