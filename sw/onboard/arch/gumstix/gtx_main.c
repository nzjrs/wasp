#include <glib.h>

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


