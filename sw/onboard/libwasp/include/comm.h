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

extern SystemStatus_t           comm_system_status;

void comm_send_ch ( CommChannel_t chan, uint8_t c );
void comm_send_message_ch ( CommChannel_t chan, uint8_t c );
void comm_start_message ( CommChannel_t chan, uint8_t id, uint8_t len );
void comm_end_message ( CommChannel_t chan );
void comm_init (uint8_t acid);
const CommMessage_t *comm_parse (uint8_t *data, uint8_t len);

#endif /* COMM_H */

