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
#include <stdio.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "autopilot.h"

#include "generated/settings.h"

#include "lib/time_helpers.h"

#include "nps_fdm.h"
#include "nps_flightgear.h"
#include "nps_global.h"
#include "nps_sensors.h"
#include "nps_state.h"

static bool_t enabled = FALSE;

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

static GTimer *fg_timer;

void hw_init(void)
{
    g_thread_init(NULL);

    time_helpers_init();

    /* sys_time.h */
    cpu_usage = 0;
    cpu_time_sec = 0;

    /* nps specific */
    sim.time = 0.0;
    fg_timer = g_timer_new();  
    nps_fdm_init(PERIODIC_TASK_DT);
    nps_flightgear_init(NPS_FLIGHTGEAR_HOST, NPS_FLIGHTGEAR_PORT);
    nps_state_init(TRUE);
}

/* This is baiscally the main loop, this function gets called very fast */
bool_t sys_time_periodic( void ) 
{
    gulong sleep_time;
    bool_t should_run;
    gdouble fg_elapsed_sec;

    sim.time = time_helpers_check_periodic(&should_run, &cpu_usage, &sleep_time);
    cpu_time_sec = sim.time;

    //FIXME: Temp hack for testing...
    if (cpu_time_sec > 20 && !enabled) {
        led_log("ENABLING AUTOPILOT");
        autopilot_set_mode(AP_MODE_ATTITUDE_DIRECT);
        autopilot_set_motors(TRUE);
        enabled = TRUE;
    }

    /* copy state from the FDM */
    nps_fdm_run_step();
    nps_sensors_run_step(sim.time);
    nps_state_update();

    /* Update flightgear */
    fg_elapsed_sec = g_timer_elapsed(fg_timer, NULL);
    if (fg_elapsed_sec > (1.0 / NPS_FLIGHTGEAR_UPDATE_FREQUENCY)) {
        g_timer_start(fg_timer);
        nps_flightgear_send();
    }

    if (should_run == FALSE)
        time_helpers_sleep(sleep_time);
        
    return should_run;
}

