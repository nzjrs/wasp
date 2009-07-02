import ppz
import ppz.transport as transport
import ppz.messages as messages
import ppz.monitor as monitor

class UAVSource(monitor.GObjectSerialMonitor):
    def __init__(self):
        t = transport.Transport(check_crc=True, debug=options.debug)

