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
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include <glib.h>
#include <glib/gstdio.h>

#include "std.h"
#include "comm.h"

#include "generated/messages.h"
#include "generated/settings.h"

/* Only provide an implementation for COMM_TELEMETRY, aka
 * the XBEE, which is used for telemetry. This implementation is 2
 * local FIFOs in /tmp which other processes can read/write to 
 *
 * FIFOs are unidirectional so two are created, one each for write and read
 *     - /tmp/WASP_COMM_XXX_SOGI      (SOGI = sim-out-groundstation-in)
 *     - /tmp/WASP_COMM_XXX_SIGO      (SIGO = sim-in-groundstation-out)
 */

#define FIFO_PATH   "/tmp/WASP_"
#define FIFO_WRITE  FIFO_PATH"COMM_TELEMETRY_SOGI"
#define FIFO_READ   FIFO_PATH"COMM_TELEMETRY_SIGO"

SystemStatus_t  comm_system_status;
int             write_fd;
int             read_fd;

/* simple circular buffer for comm, insert char into head,
 pull from tail */
#define CBUF_SIZE   256
uint8_t             read_buf[CBUF_SIZE];
uint8_t             read_head;
uint8_t             read_tail;

static bool_t make_fifo(const char *path)
{
    int i;

    /* safety check, we unlink if the file exists, so make sure
     * we can only do that in /tmp, not on /home */
    if ( ! g_str_has_prefix(path, g_get_tmp_dir()) ) {
        g_warning("FIFO must be in tmp dir");
        return FALSE;
    }

    if ( g_file_test(path, G_FILE_TEST_EXISTS) ) {
        if ( g_unlink(path) != 0 ) {
            g_warning("ERROR deleting old FIFO: %s", path);
            return FALSE;
        }
    }

    i = mkfifo(path, 0666);
    if (i != 0) {
        g_warning("Could not create FIFO: %s (%s)", path, strerror(errno));
        return FALSE;
    }

    return TRUE;
}

void comm_init ( CommChannel_t chan )
{
    int i;

    if (chan == COMM_TELEMETRY) {
        if (make_fifo(FIFO_WRITE) && make_fifo(FIFO_READ)) {
            /* Open the write end with O_RDWR, to prevent errors when writing 
             * to it before the groundstation has opened it for reading */
            write_fd = open(FIFO_WRITE, O_RDWR | O_NONBLOCK);
            /* Open the read end normally */
            read_fd = open(FIFO_READ, O_RDONLY | O_NONBLOCK);
            /* mark channel as used */
            comm_channel_used[chan] = (write_fd != -1 && read_fd != -1);
        } else 
            comm_system_status = STATUS_FAIL;
    }

    for (i = 0; i < COMM_NB; i++) {
        comm_callback_rx[i] = 0;
        comm_callback_tx[i] = 0;
    
        comm_status[i].parse_state = STATE_UNINIT;
        comm_status[i].msg_received = FALSE;
        comm_status[i].buffer_overrun = 0;
        comm_status[i].parse_error = 0;
    }

    comm_system_status = STATUS_INITIALIZED;

    read_head = read_tail = 0;

}

bool_t comm_ch_available ( CommChannel_t chan )
{
    /* read one byte at a time */
    if ((chan == COMM_TELEMETRY) && (comm_system_status == STATUS_INITIALIZED)) {
        uint8_t ch;
        int i;

        i = read(read_fd, &read_buf[read_head], 1);
        if (i == 1)
            read_head = (read_head + 1) % CBUF_SIZE;

        return read_head > read_tail;
    }

    return FALSE;
}

void comm_send_ch (CommChannel_t chan, uint8_t c)
{
    if ((chan == COMM_TELEMETRY) && (comm_system_status == STATUS_INITIALIZED))
        if (write(write_fd, &c, 1) != 1)
            g_warning("Write error");
}

uint8_t comm_get_ch(CommChannel_t chan)
{
    if ((chan == COMM_TELEMETRY) && (comm_system_status == STATUS_INITIALIZED)) {
        uint8_t c;

        c = read_buf[read_tail];
        read_tail = (read_tail + 1) % CBUF_SIZE;

        return c;
    }

    return '\0';
}

bool_t comm_check_free_space ( CommChannel_t chan, uint8_t len )
{
    return TRUE;
}

void comm_overrun ( CommChannel_t chan ) 
{
    ;
}
