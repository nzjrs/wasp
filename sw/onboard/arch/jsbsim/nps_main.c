/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */
#include <glib.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"

#include "generated/settings.h"

#include "nps_fdm.h"
#include "nps_flightgear.h"

typedef struct __SIM {
    GTimer          *started;
    GTimer          *timer;
    GTimer          *fg_timer;
} SIM_t;

/* The main entry point for the sim, largely equivilent to main() is hw_init.
 * 
 * However the sim complexity is also due ot it running in a seperate thread
 * to the autopilot. For example, all 'onboard code' runs in the main thread, 
 * as described by all calls in autopilot_main.c. Meanwhile, there is a second
 * thread that actually performs the FDM. Data is copied from FDM thread to the
 * main thread each time step (sys_time_periodic). Therefor, the main coupling
 * between the FDM and the autopilot is through sys_time_periodic */

SIM_t       sim;
uint16_t    cpu_time_sec;
uint8_t     cpu_usage;

#include <stdio.h>

void hw_init(void)
{
    g_thread_init(NULL);

    sim.started = g_timer_new();
    sim.timer = g_timer_new();
    sim.fg_timer = g_timer_new();  

    nps_fdm_init(PERIODIC_TASK_DT);
    nps_flightgear_init(NPS_FLIGHTGEAR_HOST, NPS_FLIGHTGEAR_PORT);
}

bool_t sys_time_periodic( void ) 
{
    bool_t ret;
    gdouble elapsed_sec, fg_elapsed_sec;

    elapsed_sec = g_timer_elapsed(sim.timer, NULL); 
    cpu_time_sec = g_timer_elapsed(sim.started, NULL);
    cpu_usage = 0;

    if (elapsed_sec > PERIODIC_TASK_DT) {
        /* reset the timer */
        g_timer_start(sim.timer);
        ret = TRUE;
    } else {
        ret = FALSE;
    }

    /* Update flightgear */
    fg_elapsed_sec = g_timer_elapsed(sim.fg_timer, NULL);
    if (fg_elapsed_sec > (1.0 / NPS_FLIGHTGEAR_UPDATE_FREQUENCY)) {
        g_timer_start(sim.fg_timer);
        nps_flightgear_send();
    }

    /* sleep for 1/4 of the time remaining before we need to run again */
    if (ret == FALSE) {
        g_usleep((PERIODIC_TASK_DT - elapsed_sec) * 0.25 * G_USEC_PER_SEC);
        ret = FALSE;
    }


    return ret;
}

