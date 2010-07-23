#ifndef _NPS_GLOBAL_H_
#define _NPS_GLOBAL_H_

#include <glib.h>

typedef struct __SIM {
    GTimer          *started;
    gdouble         time;
} SIM_t;

extern SIM_t    sim;

#endif /* _NPS_GLOBAL_H_ */

