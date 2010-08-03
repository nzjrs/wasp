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
#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "generated/messages.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );
bool_t test_message_tx ( CommChannel_t chan, uint8_t msgid );
bool_t test_message_rx (CommChannel_t chan, CommMessage_t *message);

#define DA_COMM COMM_TELEMETRY

/*
    <message name="TEST_MESSAGE" id="26">
        <field name="a_uint8" type="uint8"></field>
        <field name="a_int8" type="int8"></field>
        <field name="a_uint16" type="uint16"></field>
        <field name="a_int16" type="int16"></field>
        <field name="a_uint32" type="uint32"></field>
        <field name="a_int32" type="int32"></field>
        <field name="a_float" type="float"></field>
        <field name="array_uint16" type="uint16[2]"></field>
        <field name="array_uint32" type="uint32[2]"></field>
        <field name="array_float" type="float[2]"></field>
        <field name="another_uint8" type="uint8"></field>
    </message>
*/
static uint8_t u8 = 1; static uint8_t i8 = -1;
static uint16_t u16 = 10; static int16_t i16 = -10;
static uint32_t u32 = 100; static int32_t i32 = -100;
static float f = 1.0;
static uint16_t array_u16[2] = {1,2};
static uint32_t array_u32[2] = {3,4};
static float array_float[2] = {5.0,6.0};
static uint8_t another_u8 = 1;

int main( void ) {
  main_init();
  while(1) {
    if (sys_time_periodic())
      main_periodic_task();
    main_event_task();
  }
  return 0;
}

bool_t
test_message_tx ( CommChannel_t chan, uint8_t msgid )
{
    if (msgid == MESSAGE_ID_TEST_MESSAGE)
    {
        MESSAGE_SEND_TEST_MESSAGE (DA_COMM, &u8, &i8, &u16, &i16, &u32, &i32, &f, array_u16, array_u32, array_float, &another_u8 );
        return TRUE;
    }
    return FALSE;
}

bool_t
test_message_rx (CommChannel_t chan, CommMessage_t *message)
{

    if (message && message->msgid == MESSAGE_ID_TEST_MESSAGE) 
    {
        uint8_t *payload = message->payload;

	    led_toggle(2);

        u8 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_uint8(payload);
        i8 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_int8(payload);
        u16 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_uint16(payload);
        i16 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_int16(payload);
        u32 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_uint32(payload);
        i32 = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_int32(payload);
        f = MESSAGE_TEST_MESSAGE_GET_FROM_BUFFER_a_float(payload);
    }
    return FALSE;
}

static inline void main_init( void ) {
    hw_init();
    sys_time_init();
    led_init();

    comm_init(DA_COMM);
    comm_add_tx_callback(DA_COMM, test_message_tx);
    comm_add_rx_callback(DA_COMM, test_message_rx);

    int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(DA_COMM);

    RunOnceEvery(200, {
        led_toggle(4);
        MESSAGE_SEND_TEST_MESSAGE (DA_COMM, &u8, &i8, &u16, &i16, &u32, &i32, &f, array_u16, array_u32, array_float, &another_u8 );
    })
}

static inline void main_event_task( void ) {
  comm_event_task(DA_COMM);
}
