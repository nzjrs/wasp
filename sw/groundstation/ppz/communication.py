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
