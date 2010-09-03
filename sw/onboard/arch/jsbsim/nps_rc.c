#include "std.h"
#include "rc.h"
#include "led.h"

#include "nps_global.h"
#include "nps_rc_joystick.h"

#include <glib.h>
#include <glib/gprintf.h>

#define NPS_RC_SCRIPT_FREQ 20
typedef void (*RCScriptFunc)(double);

typedef struct __NpsRC {
    GThread         *thread;
    GMainContext    *context;
    GMainLoop       *loop;
    char            *joystick_device;
    RCScriptFunc    script_func;
} NpsRC_t;
static NpsRC_t nps_rc_state;

/* these so-called script functions are simple ways to input RC values */
static void radio_control_script_takeoff(double time);


SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

static gboolean rc_run_script(gpointer data)
{
    NpsRC_t *state = (NpsRC_t *)data;
    rc_status = RC_OK;
    rc_system_status = STATUS_ALIVE;
    state->script_func(sim.time);
    return TRUE;
}

static gpointer rc_mainloop_thread(gpointer data)
{
    gboolean rc_ok;
    NpsRC_t *state = (NpsRC_t *)data;

    state->context = g_main_context_new();
    state->loop = g_main_loop_new(state->context, FALSE);

    if (state->joystick_device) {
        led_log("RC: Using Joystick %s\n", state->joystick_device);
        /* init the joystick device, it uses io_add_watch, so it needs the context */
        rc_ok = nps_radio_control_joystick_init(state->joystick_device, state->context);
        if (rc_ok)
            rc_system_status = STATUS_INITIALIZED;
    } else if (state->script_func) {
        /* start a regular timer */
        led_log("RC: Using script function\n");
        GSource *timeout = g_timeout_source_new (1000/NPS_RC_SCRIPT_FREQ);
        g_source_set_callback(timeout, (GSourceFunc)rc_run_script, state, NULL);
        g_source_attach(timeout, state->context);
        rc_system_status = STATUS_INITIALIZED;
    }

    /* start the mainloop */
    g_main_loop_run(state->loop);
    return NULL;
}

void rc_init ( void )
{
    int i;

    /* init the RC state */
    for (i = 0; i < RADIO_CTL_NB; i++) {
        rc_values[i] = 0;
        ppm_pulses[i] = 0;
    }
    rc_status = RC_REALLY_LOST;

#if 1
    nps_rc_state.joystick_device = g_strdup("/dev/input/js0");
    nps_rc_state.script_func = NULL;
#else
    nps_rc_state.joystick_device = NULL;
    nps_rc_state.script_func = radio_control_script_takeoff;
#endif

    nps_rc_state.thread = g_thread_create(rc_mainloop_thread, &nps_rc_state, FALSE, NULL);
}

void rc_periodic_task ( void )
{

}

bool_t
rc_event_task ( void )
{
    return TRUE;
}

/*
 * Scripts
 */

void radio_control_script_takeoff(double time)
{
    rc_values[RADIO_ROLL] = 0;
    rc_values[RADIO_PITCH] = 0;

    /* starts motors after 5 seconds, then throttles up */
    if (time > 5. && time < 6.)
        rc_values[RADIO_YAW] = MIN_PPRZ;
    else if (time > 6.)
        rc_values[RADIO_YAW] = 0;
    
    if (time > 9.)
        rc_values[RADIO_THROTTLE] = 0.6 * MAX_PPRZ;

}
