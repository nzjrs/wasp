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
#ifndef  MESSAGES_H
#define  MESSAGES_H

#include "std.h"

#define COMM_MAX_PAYLOAD_LEN 256

typedef enum {
    COMM_0,
    COMM_TELEMETRY,
    COMM_USB,
    COMM_NB
} CommChannel_t;

/**
 * Description of a periodic message.
 */
typedef struct __PeriodicMessage {
    uint16_t        target;
    uint16_t        cnt;
    uint8_t         msgid;
    CommChannel_t   chan;
} PeriodicMessage_t;

/**
 * A message to be sent.
 */
typedef struct __CommMessage {
    uint8_t acid;   /**< Aircraft ID, id of message sender */
    uint8_t msgid;  /**< ID of message in payload */
    uint8_t len;    /**< Length of payload */
    uint8_t payload[COMM_MAX_PAYLOAD_LEN] __attribute__ ((aligned));    /**< Payload */
    uint8_t ck_a;   /**< Checksum high byte */
    uint8_t ck_b;   /**< Checksum low byte */
    uint8_t idx;    /**< State vaiable when filling payload. Not sent */
} CommMessage_t;

typedef enum {
    STATE_UNINIT,
    STATE_GOT_STX,
    STATE_GOT_LENGTH,
    STATE_GOT_ACID,
    STATE_GOT_MSGID,
    STATE_GOT_PAYLOAD,
    STATE_GOT_CRC1
} ParseState_t;
    
typedef struct __CommStatus {
    uint8_t ck_a;
    uint8_t ck_b;
    uint8_t msg_received;
    uint8_t buffer_overrun;
    uint8_t parse_error;
    ParseState_t parse_state;
} CommStatus_t;

typedef bool_t (*CommRXMessageCallback_t)(CommChannel_t chan, CommMessage_t *message);
typedef bool_t (*CommTXMessageCallback_t)(CommChannel_t chan, uint8_t msgid);

#endif /* MESSAGES_H */
