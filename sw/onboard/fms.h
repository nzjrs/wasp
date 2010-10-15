#ifndef _FMS_H_
#define _FMS_H_

#include "std.h"
#include "messages_types.h"
#include "math/pprz_algebra_int.h"

typedef struct __FMSCommand {
    union {
        struct Int32Vect3   rate;
        struct Int32Eulers  attitude;
        struct Int32Vect2   speed;
        struct Int32Vect3   pos;          //FIXME Warning z is heading
    } h_sp;
    union {
        int32_t direct;
        int32_t climb;
        int32_t height;
    } v_sp;
} FMSCommand_t;

typedef struct __FMS {
    FMSCommand_t    command;
    bool_t          enabled_rc;
    bool_t          enabled_msg;
    uint8_t         mode;
    bool_t          timeout;
    uint8_t         last_msg;
} FMS_t;

extern FMS_t            fms;
extern SystemStatus_t   fms_system_status;

void fms_init(void);
void fms_periodic_task(void);
void fms_set(CommMessage_t *message);
bool_t fms_is_enabled(void);
void fms_msg_enable(bool_t enabled);

#endif /* _FMS_H_ */
