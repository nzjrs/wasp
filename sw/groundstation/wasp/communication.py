import random
import os
import gobject
import serial

import libserial.SerialSender

import wasp

class SerialCommunication(libserial.SerialSender.SerialSender):
    """
    Reads data from the serial port 
    """
    def read(self, nbytes=5):
        if self.is_open():
            try:
                return self._serial.read(nbytes)
            except  serial.SerialTimeoutException:
                pass
        return ""
    
    def write(self, data):
        if self.is_open():
            self._serial.write(data)

class DummySerialCommunication(gobject.GObject):
    """
    For testing groundstation with no UAV
    """

    __gsignals__ = {
        "serial-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_BOOLEAN]),     #True if successfully connected to the port
        }

    def __init__(self, messages, transport, header):
        gobject.GObject.__init__(self)
        self._readfd, self._writefd = os.pipe()

        self._messages = messages        
        self._transport = transport
        self._header = header

        self._sendcache = {}

        #Write messages to the pipe, so that it is read and processed by
        #the groundstation
        #
        #TIME at 1hz
        self._t = 0
        gobject.timeout_add(int(1000/0.1), self._do_time)
        #STATUS, COMM_STATUS at 0.5hz
        self._generic_send(int(1000/0.5), "STATUS")
        self._generic_send(int(1000/0.5), "COMM_STATUS")
        #IMU at 10hz
        self._generic_send(int(1000/10), "IMU_ACCEL_RAW")
        self._generic_send(int(1000/10), "IMU_MAG_RAW")
        self._generic_send(int(1000/10), "IMU_GYRO_RAW")
        #AHRS at 10hz
        gobject.timeout_add(int(1000/10), self._do_ahrs)
        #GPS at 4 Hz
        gobject.timeout_add(int(1000/4), self._do_gps)
        self._alt = wasp.NoisySine(freq=0.5, value_type=int)
        self._lat = -43.520451
        self._lon = 172.582377

    def _do_gps(self):

        if random.randint(0,4) == 4:
            self._lat += (random.random()*0.0001)
        if random.randint(0,4) == 4:
            self._lon += (random.random()*0.0001)

        lat = int(self._lat * 1e7)
        lon = int(self._lon * 1e7)
        alt = self._alt.value() * 1000.0

        msg = self._messages.get_message_by_name("GPS_LLH")
        return self._send(msg, 2, 5, lat, lon, alt, 1, 1)

    def _do_generic_send(self, msgname):
        msg, vals = self._sendcache[msgname]
        self._send(msg, *vals)
        return True

    def _generic_send(self, freq, msgname):
        msg = self._messages.get_message_by_name(msgname)
        if msg:
            self._sendcache[msgname] = (msg, msg.get_default_values())
            gobject.timeout_add(freq, self._do_generic_send, msgname)

    def _send(self, msg, *vals):
        data = self._transport.pack_message_with_values(
                        self._header,
                        msg,
                        *vals)
        os.write(self._writefd, data.tostring())
        return True

    def _do_time(self):
        self._t += 10
        msg = self._messages.get_message_by_name("TIME")
        return self._send(msg, self._t)

    def _do_ahrs(self):
        return True

    def get_fd(self):
        return self._readfd

    def connect_to_port(self):
        self.emit("serial-connected", True)
        return True

    def disconnect_from_port(self):
        self.emit("serial-connected", False)

    def write(self, data):
        os.write(self._writefd, data)

    def read(self, nbytes=5):
        return os.read(self._readfd, nbytes)




