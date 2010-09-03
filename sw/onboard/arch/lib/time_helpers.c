#include <glib.h>

#include "std.h"

#include "generated/settings.h"

#include "time_helpers.h"

static GTimer *started;
static GTimer *loop_timer;

/* used to guestimate if the PC running the sim is too slow. If we have to
run every time, i.e. we can't keep up with PERIODIC_TASK_DT then we are not
really being a true SITL */
uint32_t    nth_time_run;

void
time_helpers_init(void)
{
    started = g_timer_new();
    loop_timer = g_timer_new();
}

gdouble
time_helpers_check_periodic(bool_t *should_run, uint8_t *cpu_usage, gulong *sleep_time)
{
    gdouble elapsed_sec;

    elapsed_sec = g_timer_elapsed(loop_timer, NULL);
    if (elapsed_sec > PERIODIC_TASK_DT) {
        /* reset the timer */
        g_timer_start(loop_timer);
        *should_run = TRUE;
        switch(nth_time_run) {
            case 0:
                *cpu_usage = 100;
                break;
            /* these are just made up numbers */
            case 1:
                *cpu_usage = 75;
                break;
            case 2:
                *cpu_usage = 50;
                break;
            case 3:
                *cpu_usage = 25;
                break;
            default:
                *cpu_usage = 0;
                break;
        }
        nth_time_run = 0;
    } else {
        /* The main loop should not run */
        *should_run = FALSE;
        nth_time_run += 1;
        /* sleep for 1/4 of the time remaining before we need to run again */
        *sleep_time = (gulong)((PERIODIC_TASK_DT - elapsed_sec) * 0.25 * G_USEC_PER_SEC);
    }

    return g_timer_elapsed(started, NULL);
}

void time_helpers_sleep(gulong sleep_time)
{
    g_usleep(sleep_time);
}
