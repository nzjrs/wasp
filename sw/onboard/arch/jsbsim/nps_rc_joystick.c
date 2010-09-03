#include <glib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <glib.h>
#include <glib/gprintf.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/joystick.h>

#include "rc.h"
#include "generated/radio.h"
#include "nps_rc_joystick.h"

typedef struct __NpsJoystickAxis {
    int     reverse;
    char    *name;
} NpsJoystickAxis_t;

typedef struct __NpsJoystick {
    char                *name;
    NpsJoystickAxis_t   axis[RADIO_CTL_NB];
    int                 num_axis;
} NpsJoystick_t;

static NpsJoystick_t    nps_joystick;

static gboolean on_js_data_received(GIOChannel *source, 
				                    GIOCondition condition __attribute__ ((unused)), 
				                    gpointer data __attribute__ ((unused)))
{
    struct js_event js;
    gsize len;
    GError *err = NULL;

    g_io_channel_read_chars(
            source,
            (gchar*)(&js),
            sizeof(struct js_event),
            &len, &err);

    if (js.type == JS_EVENT_AXIS) {
        if (js.number < RADIO_CTL_NB) {
            /* js.number is u8, 0-indexed. The axis mapping is already handled
               by the xml, so we just need to scale to the rc range */
            NpsJoystickAxis_t *axis = &nps_joystick.axis[js.number];
            rc_values[js.number] = axis->reverse * js.value * MAX_PPRZ/INT16_MAX;
            rc_status = RC_OK;
            rc_system_status = STATUS_ALIVE;
        }
    }
    return TRUE;
}

/* The radio xml handler functions. */
static void radio_xml_start_element(GMarkupParseContext *context,
                                    const gchar         *element_name,
                                    const gchar        **attribute_names,
                                    const gchar        **attribute_values,
                                    gpointer             user_data,
                                    GError             **error)
{

    const gchar **name_cursor = attribute_names;
    const gchar **value_cursor = attribute_values;

    if (strcmp (element_name, "radio") == 0) {
        while (*name_cursor) {
            if (strcmp (*name_cursor, "name") == 0)
                nps_joystick.name = g_strdup (*value_cursor);
            name_cursor++;
            value_cursor++;
        }
    } else if (strcmp (element_name, "channel") == 0) {

        gint axis_js = -1;
        gint axis_max = 0;
        gint axis_min = 0;
        const gchar *axis_function = NULL;

        while (*name_cursor) {
            if (strcmp (*name_cursor, "ctl") == 0) {
                axis_js = g_ascii_strtod (*value_cursor, NULL);
            }
            if (strcmp (*name_cursor, "function") == 0) {
                axis_function = *value_cursor;
            }
            if (strcmp (*name_cursor, "max") == 0) {
                axis_max = g_ascii_strtod (*value_cursor, NULL);
            }
            if (strcmp (*name_cursor, "min") == 0) {
                axis_min = g_ascii_strtod (*value_cursor, NULL);
            }
            name_cursor++;
            value_cursor++;
        }

        /* radio.xml contains the assignments for the joystick axis. the mapping
        of these is already done in the xml file, so we just remember the name
        of the joystick, and if it needs to be reversed or not */
        if (axis_js != -1 && axis_function && axis_max != 0 && axis_min != 0) {
            int i = axis_js - 1;            /* make 0-indexed */
            nps_joystick.num_axis += 1;
            nps_joystick.axis[i].name = g_strdup(axis_function);
            nps_joystick.axis[i].reverse = (axis_max > axis_min ? 1 : -1);
        }

    }
}

gboolean nps_radio_control_joystick_init(const char* device, GMainContext *context)
{
    int i;
    GError *err = NULL;

    int fd = open(device, O_RDONLY | O_NONBLOCK);
    if (fd == -1) {
        g_warning("opening joystick device %s : %s\n", device, strerror(errno));
        return FALSE;
    }

    /* information about the joystick axis */
    nps_joystick.num_axis = 0;
    nps_joystick.name = NULL;
    for (i = 0; i < RADIO_CTL_NB; i++) {
        nps_joystick.axis[i].reverse = 1;
        nps_joystick.axis[i].name = NULL;
    }

    /* parse the radio.xml which describes the joystick mapping */
    GMarkupParser xml_parser_functions = { radio_xml_start_element };
    GMarkupParseContext *parser = g_markup_parse_context_new (
                                        &xml_parser_functions,
                                        G_MARKUP_DO_NOT_USE_THIS_UNSUPPORTED_FLAG,
                                        NULL,
                                        NULL);
    if (g_markup_parse_context_parse (parser, RADIO_XML, -1, &err) == FALSE) {
        g_warning("Radio XML Parse failed: %s (%d)\n", err->message, err->code);
        return FALSE;
    }

    GIOChannel* channel = g_io_channel_unix_new(fd);
    g_io_channel_set_encoding(channel, NULL, NULL);

    /* create a watch on the FD using the supplied MainContext */
    GSource *watch = g_io_create_watch(channel, G_IO_IN);
    g_source_set_callback(
        watch,
        (GSourceFunc)on_js_data_received,
        NULL,
        NULL);

    /* this means that on_js_data_received will be called when the mainloop
    associated with the context is started */
    g_source_attach(watch, context);
    return TRUE;
}

