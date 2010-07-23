#include "rc.h"
#include "nps_rc_joystick.h"

#include <glib.h>
#include <glib/gprintf.h>

typedef struct __NpsRC {
    GThread         *thread;
    GMainContext    *context;
    GMainLoop       *loop;
} NpsRC_t;
static NpsRC_t nps_rc_state;

SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

static gpointer rc_mainloop_thread(gpointer data)
{
    gboolean rc_ok;
    NpsRC_t *state = (NpsRC_t *)data;

    state->context = g_main_context_new();
    state->loop = g_main_loop_new(state->context, FALSE);

    /* start a regular timer */
    //GSource *timeout = g_timeout_source_new_seconds (1);
    //g_source_set_callback(timeout, (GSourceFunc)ping, NULL, NULL);
    //g_source_attach(timeout, state->context);

    /* init the joystick device, it uses io_add_watch, so it needs the context */
    rc_ok = nps_radio_control_joystick_init("/dev/input/js0", state->context);
    if (rc_ok)
        rc_system_status = STATUS_INITIALIZED;

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

    nps_rc_state.thread = g_thread_create(rc_mainloop_thread, &nps_rc_state, FALSE, NULL);
}

void rc_periodic_task ( void )
{

}

bool_t
rc_event_task ( void )
{
    return FALSE;
}
