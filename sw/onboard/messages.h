#ifndef  MESSAGES_H
#define  MESSAGES_H

#include "std.h"

#define COMM_MAX_PAYLOAD_LEN 256

typedef enum {
    COMM_0,         /**< UART0, the GPS */
    COMM_1,         /**< UART1, the XBEE */
    COMM_USB,       /**< USB */
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
    uint8_t payload[COMM_MAX_PAYLOAD_LEN] __attribute__ ((aligned));
    uint8_t ck_a;   /**< Checksum high byte */
    uint8_t ck_b;   /**< Checksum low byte */
    uint8_t idx;    /**< State vaiable when filling payload. Not sent */
} CommMessage_t;

#endif /* MESSAGES_H */
