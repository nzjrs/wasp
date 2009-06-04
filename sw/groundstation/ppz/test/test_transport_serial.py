import testsetup
import ppz.transport as transport

p = transport.SerialTransport(port="/dev/ttyUSB0", speed=57600)
p.connect()

if p.is_open():
    print p.read()
p.disconnect()
