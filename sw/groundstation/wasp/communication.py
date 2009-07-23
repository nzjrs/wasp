import random
import os
import gobject
import serial
import libserial.SerialSender

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

        #Write messages to the pipe, so that it is read and processed by
        #the groundstation
        #
        #TIME at 0.1hz
        self._t = 0
        gobject.timeout_add(int(1000/0.1), self._do_time)
        #STATUS at 0.5hz
        gobject.timeout_add(int(1000/0.5), self._do_status)
        #IMU at 10hz
        gobject.timeout_add(int(1000/10), self._do_imu)
        #AHRS at 10hz
        gobject.timeout_add(int(1000/10), self._do_ahrs)

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

    def _do_status(self):
        msg = self._messages.get_message_by_name("STATUS")
        return self._send(msg, 0, 0, 0, 0, 0, 0)

    def _do_imu(self):
        msg = self._messages.get_message_by_name("IMU_ACCEL_RAW")
        self._send(msg, 1000, 2000, 3000)
        msg = self._messages.get_message_by_name("IMU_GYRO_RAW")
        self._send(msg, 4000, 5000, 6000)
        return True

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




