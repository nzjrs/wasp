#ifndef SETTINGS_H
#define SETTINGS_H

#include "std.h"
#include "comm.h"

bool_t
settings_init(void);

bool_t
settings_load(uint8_t id, Type_t *type, void *data);

bool_t
settings_save(uint8_t id, Type_t type, void *data);

void
settings_load_all(void);

bool_t
settings_handle_message_received(CommChannel_t chan, CommMessage_t *message);

#endif


