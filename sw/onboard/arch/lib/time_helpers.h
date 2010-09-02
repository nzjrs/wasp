#ifndef _TIME_HELPERS_H_
#define _TIME_HELPERS_H_

#include <glib.h>
#include "std.h"

void
time_helpers_init(void);

gdouble
time_helpers_check_periodic(bool_t *should_run, uint8_t *cpu_usage, gulong *sleep_time);

void
time_helpers_sleep(gulong sleep_time);

#endif /*_TIME_HELPERS_H_*/
