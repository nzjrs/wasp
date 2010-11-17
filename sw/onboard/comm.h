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
#ifndef COMM_H
#define COMM_H

#include "std.h"
#include "messages_types.h"

extern CommRXMessageCallback_t  comm_callback_rx[COMM_NB];
extern CommTXMessageCallback_t  comm_callback_tx[COMM_NB];
extern CommMessage_t            comm_message[COMM_NB];
extern CommStatus_t             comm_status[COMM_NB];
extern bool_t                   comm_channel_used[COMM_NB];
extern SystemStatus_t           comm_system_status;

void
comm_init ( CommChannel_t chan );

void
comm_set_acid (uint8_t acid);

void
comm_add_rx_callback ( CommChannel_t chan, CommRXMessageCallback_t cb);

void
comm_add_tx_callback ( CommChannel_t chan, CommTXMessageCallback_t cb);

void
comm_periodic_task ( CommChannel_t chan );

bool_t
comm_event_task ( CommChannel_t chan );

bool_t
comm_ch_available ( CommChannel_t chan );

void
comm_send_message_ch ( CommChannel_t chan, uint8_t c );

void 
comm_send_ch ( CommChannel_t chan, uint8_t c );

void
comm_send_message ( CommChannel_t chan, CommMessage_t *message );

bool_t
comm_send_message_by_id (CommChannel_t chan, uint8_t msgid);

uint8_t
comm_get_ch( CommChannel_t chan );

bool_t
comm_check_free_space ( CommChannel_t chan, uint8_t len );

void
comm_start_message ( CommChannel_t chan, uint8_t id, uint8_t len );

void
comm_end_message ( CommChannel_t chan );

bool_t
comm_parse ( CommChannel_t chan );

void
comm_overrun ( CommChannel_t chan );

void
comm_send_command_ack (CommChannel_t chan, uint8_t msgid);

void
comm_send_command_nack (CommChannel_t chan, uint8_t msgid);

void
comm_start_message_hw ( CommChannel_t chan );

void
comm_end_message_hw ( CommChannel_t chan );

#endif /* COMM_H */

