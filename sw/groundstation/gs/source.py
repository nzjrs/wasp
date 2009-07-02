import ppz
import ppz.transport as transport
import ppz.messages as messages
import ppz.monitor as monitor

DEBUG=False

class UAVSource(monitor.GObjectSerialMonitor):
    def __init__(self):
        self._serialsender = transport.SerialTransport(port="/dev/ttyUSB0", speed=57600, timeout=1)
        monitor.GObjectSerialMonitor.__init__(self, self._serialsender)

        self._transport = transport.Transport(check_crc=True, debug=DEBUG)
        self._messages_file = messages.MessagesFile(path="/home/john/Programming/wasp.git/sw/messages.xml", debug=DEBUG)
        self._messages_file.parse()

    def on_serial_data_available(self, fd, condition, serial):

        data = serial.read(1)
        for header, payload in self._transport.parse_many(data):
            msg = self._messages_file.get_message_by_id(header.msgid)
            if msg:
                print msg
            #    self._rxts.update_message(msg, payload)

        return True

    def quit(self):
        self._serialsender.disconnect_from_port()


