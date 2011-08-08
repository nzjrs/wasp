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
#include "std.h"
#include "gps.h"

#include "arm7/config.h"
#include "arm7/uart_hw.h"
#include "lib/ubx_protocol.h"

#define  UBX_FIX_NONE 0x00
#define  UBX_FIX_2D   0x02
#define  UBX_FIX_3D   0x03

typedef struct __UbxParseState {
    uint8_t     id;
    uint8_t     class;
    uint8_t     status;
    uint16_t    len;
    uint8_t     msg_idx;
    uint8_t     ck_a;
    uint8_t     ck_b;
    bool_t      msg_available;
} UbxParseState_t;

typedef enum {
    GOT_MSG_GPS_POS                 = (1 << 0), /* Position message, e.g. POSLLH */
    GOT_MSG_GPS_SOL                 = (1 << 1), /* Nav solution message */
    GOT_MSG_GPS_VEL                 = (1 << 2), /* Any velocity message */
    GOT_MSG_GPS_STATUS              = (1 << 3), /* Any status message   */
} UbxGotMsgFlags;
#define UbxGotAllMsg	(GOT_MSG_GPS_POS | GOT_MSG_GPS_SOL | GOT_MSG_GPS_VEL | GOT_MSG_GPS_STATUS)

static void ubx_parse( uint8_t c );

GPS_t           gps_state;
SystemStatus_t  gps_system_status = STATUS_UNINITIAIZED;
UbxGotMsgFlags  gps_got_msgs = 0;

/* UBX parsing */
#define UBX_MAX_PAYLOAD 255
static uint8_t ubx_msg_buf[UBX_MAX_PAYLOAD] __attribute__ ((aligned));
#define UNINIT        0
#define GOT_SYNC1     1
#define GOT_SYNC2     2
#define GOT_CLASS     3
#define GOT_ID        4
#define GOT_LEN1      5
#define GOT_LEN2      6
#define GOT_PAYLOAD   7
#define GOT_CHECKSUM1 8
static UbxParseState_t ubx_state;

void gps_init(void) 
{
    uart0_init_tx();

    ubx_state.status = UNINIT;
    ubx_state.msg_available = FALSE;
    gps_system_status = STATUS_INITIALIZING;
    gps_got_msgs = 0;
    gps_state.fix = GPS_FIX_NONE;
    gps_state.buffer_overrun = 0;
    gps_state.parse_error = 0;
    gps_state.parse_ignored = 0;
#if RECORD_NUM_SAT_INFO
    gps_state.num_sat_info = 0;
#endif
}

bool_t
gps_event_task(void) 
{
    if (Uart0ChAvailable()) {
        while ( Uart0ChAvailable() && !ubx_state.msg_available )
            ubx_parse(Uart0Getch());
    }

    if (ubx_state.msg_available) {
        if (ubx_state.class == UBX_NAV_ID) {
            switch (ubx_state.id) {
                case UBX_NAV_POSLLH_ID:
                    gps_got_msgs |= GOT_MSG_GPS_POS;

                    gps_state.lon = UBX_NAV_POSLLH_LON(ubx_msg_buf);
                    gps_state.lat = UBX_NAV_POSLLH_LAT(ubx_msg_buf);
                    gps_state.hmsl = UBX_NAV_POSLLH_HMSL(ubx_msg_buf);
                    gps_state.hacc = UBX_NAV_POSLLH_Hacc(ubx_msg_buf);
                    gps_state.vacc = UBX_NAV_POSLLH_Vacc(ubx_msg_buf);
                    break;
                case UBX_NAV_SOL_ID:
                    {
                    gps_got_msgs |= GOT_MSG_GPS_SOL;

                    uint8_t fix = UBX_NAV_SOL_GPSfix(ubx_msg_buf);
                    if ( fix == UBX_FIX_3D)
                        gps_state.fix = GPS_FIX_3D;
                    else if ( fix == UBX_FIX_2D )
                        gps_state.fix = GPS_FIX_2D;
                    else
                        gps_state.fix = GPS_FIX_NONE;
                    gps_state.ecef_pos.x   = UBX_NAV_SOL_ECEF_X(ubx_msg_buf);
                    gps_state.ecef_pos.y   = UBX_NAV_SOL_ECEF_Y(ubx_msg_buf);
                    gps_state.ecef_pos.z   = UBX_NAV_SOL_ECEF_Z(ubx_msg_buf);
                    gps_state.pacc         = UBX_NAV_SOL_Pacc(ubx_msg_buf);
                    gps_state.ecef_speed.x = UBX_NAV_SOL_ECEFVX(ubx_msg_buf);
                    gps_state.ecef_speed.y = UBX_NAV_SOL_ECEFVY(ubx_msg_buf);
                    gps_state.ecef_speed.z = UBX_NAV_SOL_ECEFVZ(ubx_msg_buf);
                    gps_state.sacc         = UBX_NAV_SOL_Sacc(ubx_msg_buf);
                    gps_state.pdop         = UBX_NAV_SOL_PDOP(ubx_msg_buf);
                    gps_state.num_sv       = UBX_NAV_SOL_numSV(ubx_msg_buf);
                    }
                    break;
                case UBX_NAV_VELNED_ID:
                    gps_got_msgs |= GOT_MSG_GPS_VEL;

                    gps_state.vel_n = UBX_NAV_VELNED_VEL_N(ubx_msg_buf);
                    gps_state.vel_e = UBX_NAV_VELNED_VEL_E(ubx_msg_buf);
                    break;
                case UBX_NAV_SVINFO_ID:
                    {
#if RECORD_NUM_SAT_INFO
                    uint8_t i;
                    uint8_t nch = UBX_NAV_SVINFO_NCH(ubx_msg_buf);
                    gps_state.num_sat_info = Min(nch, RECORD_NUM_SAT_INFO);
                    for (i = 0; i < gps_state.num_sat_info; i++) {
                        gps_state.sat_info[i].sat_id = UBX_NAV_SVINFO_SVID(ubx_msg_buf, i);
                        gps_state.sat_info[i].elevation = UBX_NAV_SVINFO_Elev(ubx_msg_buf, i);
                        gps_state.sat_info[i].azimuth = UBX_NAV_SVINFO_Azim(ubx_msg_buf, i);
                        gps_state.sat_info[i].signal_strength = UBX_NAV_SVINFO_CNO(ubx_msg_buf, i);
                    }
#endif
                    }
                    break;
                case UBX_NAV_STATUS_ID:
                    /* FIXME: Maybe use fix from here? */
                    gps_got_msgs |= GOT_MSG_GPS_STATUS;
                    break;
                default:
                    gps_state.parse_ignored++;
                    break;
            }
        } else {
            gps_state.parse_ignored++;
        }

        gps_system_status = (gps_got_msgs == UbxGotAllMsg ? STATUS_ALIVE : STATUS_INITIALIZED);
        ubx_state.msg_available = FALSE;
        return TRUE;
    }
    return FALSE;
}

static void ubx_parse( uint8_t c )
{
    if (ubx_state.status < GOT_PAYLOAD) {
        ubx_state.ck_a += c;
        ubx_state.ck_b += ubx_state.ck_a;
    }

    switch (ubx_state.status)
    {
        case UNINIT:
            if (c == UBX_SYNC1)
                ubx_state.status++;
            break;
        case GOT_SYNC1:
            if (c != UBX_SYNC2) {
                gps_state.parse_error++;
                goto error;
            }
            ubx_state.ck_a = 0;
            ubx_state.ck_b = 0;
            ubx_state.status++;
            break;
        case GOT_SYNC2:
            if (ubx_state.msg_available) {
                /* Previous message has not yet been parsed: discard this one */
                gps_state.buffer_overrun++;
                goto error;
            }
            ubx_state.class = c;
            ubx_state.status++;
            break;
        case GOT_CLASS:
            ubx_state.id = c;
            ubx_state.status++;
            break;
        case GOT_ID:
            ubx_state.len = c;
            ubx_state.status++;
            break;
        case GOT_LEN1:
            ubx_state.len |= (c<<8);
            if (ubx_state.len > UBX_MAX_PAYLOAD) {
                gps_state.parse_error++;
                goto error;
            }
            ubx_state.msg_idx = 0;
            ubx_state.status++;
            break;
        case GOT_LEN2:
            ubx_msg_buf[ubx_state.msg_idx] = c;
            ubx_state.msg_idx++;
            if (ubx_state.msg_idx >= ubx_state.len) {
                ubx_state.status++;
            }
            break;
        case GOT_PAYLOAD:
            if (c != ubx_state.ck_a) {
                gps_state.parse_error++;
                goto error;
            }
            ubx_state.status++;
            break;
        case GOT_CHECKSUM1:
            if (c != ubx_state.ck_b) {
                gps_state.parse_error++;
                goto error;
            }
            ubx_state.msg_available = TRUE;
            goto restart;
            break;
    }
    return;
error:
restart:
    ubx_state.status = UNINIT;
    return;
}
