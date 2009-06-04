import array
import serial
import libserial.SerialSender

class SerialTransport(libserial.SerialSender.SerialSender):
    """
    Reads data from the serial port 
    """
    def read(self, nbytes=5):
        if self.is_open():
            try:
                return self._serial.read(nbytes)
            except  serial.SerialTimeoutException:
                print "Timeout"
        return ""
    
    def write(self, data):
        if self.is_open():
            self._serial.write(data)


class TransportParser:
    """
    Class that extracts a paparazzi payload from a string or 
    sequence of characters from the transport layer
    
    Data is expected in the following form

    Transport
    |STX|length|... payload=(length-4) bytes ...|Checksum A|Checksum B|
    
    Payload
    |AC_ID|MESSAGE_ID|... MESSAGE DATA ...|
    
    Data sent in little endian byte order
    """

    STATE_UNINIT = 0
    STATE_GOT_STX = 1
    STATE_GOT_LENGTH = 2
    STATE_GOT_PAYLOAD = 3
    STATE_GOT_CRC1 = 4

    def __init__(self, check_crc=True, debug=False):
        self._check_crc = check_crc
        self._debug = debug
        self._buf = array.array('c','\0'*256)
        self._state = self.STATE_UNINIT
        self._payload_len = 0
        self._payload_idx = 0
        self._ck_a = 0
        self._ck_b = 0
        self._error = 0

    def parse_many(self, string):
        """
        Similar to parse_one, but operates on a string, returning 
        multiple payloads if successful

        @returns: A list payloads
        """
        payloads = []
        for c in string:
            p = self.parse_one(c)
            if p:
                payloads.append(p)
        return payloads

    def parse_one(self, c):
        """
        Attempts to parse one character. Returns just the payload, and
        not the data in the transport layer, i.e. it does not return
        STX, the length, or the checksums

        @returns: The payload, or an empty string if insuficcient data
        is available
        """

        # Adapted from pprz_transport.h
        #  switch (pprz_status) {
        #  case UNINIT:
        #    if (c == STX)
        #      pprz_status++;
        #    break;
        #  case GOT_STX:
        #    if (pprz_msg_received) {
        #      pprz_ovrn++;
        #      goto error;
        #    }
        #    pprz_payload_len = c-4; /* Counting STX, LENGTH and CRC1 and CRC2 */
        #    _ck_a = _ck_b = c;
        #    pprz_status++;
        #    payload_idx = 0;
        #    break;
        #  case GOT_LENGTH:
        #    pprz_payload[payload_idx] = c;
        #    _ck_a += c; _ck_b += _ck_a;
        #    payload_idx++;
        #    if (payload_idx == pprz_payload_len)
        #      pprz_status++;
        #    break;
        #  case GOT_PAYLOAD:
        #    if (c != _ck_a)
        #      goto error;
        #    pprz_status++;
        #    break;
        #  case GOT_CRC1:
        #    if (c != _ck_b)
        #      goto error;
        #    pprz_msg_received = TRUE;
        #    goto restart;
        #  }
        #  return;
        # error:
        #  pprz_error++;
        # restart:
        #  pprz_status = UNINIT;
        #  return;

        payload = ""
        error = False
        #convert to 8bit int
        d = ord(c)

        if self._state == self.STATE_UNINIT:
            if d == 0x99:
                self._state += 1
        elif self._state == self.STATE_GOT_STX:
            self._payload_len = d - 4
            self._ck_a = d
            self._ck_b = d
            self._payload_idx = 0
            self._state += 1
            if self._debug: 
                print "TR LEN=%s PL LEN=%s" % (self._payload_len, d)
        elif self._state == self.STATE_GOT_LENGTH:
            self._buf[self._payload_idx] = c
            #wrap to 8bit (simulate 8 bit addition)
            self._ck_a = (self._ck_a + d) % 256
            self._ck_b = (self._ck_b + self._ck_a) % 256
            self._payload_idx += 1
            if self._payload_idx == self._payload_len:
                self._state += 1
        elif self._state == self.STATE_GOT_PAYLOAD:
            if d != self._ck_a and self._check_crc:
                error = True
                if self._debug:
                    print "CRC_A ERROR: ACID=%s MSG=%s" % (ord(self._buf[0]), ord(self._buf[1]))
            else:
                self._state += 1
        elif self._state == self.STATE_GOT_CRC1:
            if d != self._ck_b and self._check_crc:
                error = True
                if self._debug:
                    print "CRC_B ERROR"
            else:
                payload = self._buf[:self._payload_len].tostring()
                self._state = self.STATE_UNINIT

        if error:
            self._error += 1
            self._state = self.STATE_UNINIT

        return payload


