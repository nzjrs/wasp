#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import time
import os.path
import optparse
import gobject
import wasp
import wasp.transport as transport
import wasp.communication as communication
import wasp.messages as messages

import calibration
import calibration.utils

FREQ = 25.0         #Hz
STEP_DELAY = 5      #Seconds

class IMUCalibrator:
    def __init__(self, sensor, logfile, messages):
        pass

class IMULogger:

    STATES = \
        (["WAIT"] * 2 ) +\
        ["%s %s" % (o,d) for o in ("ROLL", "PITCH") for d in (90, 180, 270, 360)] +\
        (["WAIT"] * 2 )

    def __init__(self, port, messages_file, sensor_name, log_file):
        raw_imu_message_name = "IMU_%s_RAW" % sensor_name
        self.sensor_name = sensor_name
        self.m = messages.MessagesFile(path=messages_file, debug=False)
        self.m.parse()
        self.msg = self.m.get_message_by_name(raw_imu_message_name)

        if not self.msg:
            raise SystemExit("Could Not Find Message %s" % raw_imu_message_name)

        self.loop = gobject.MainLoop()
        self.state = 0

        self.measurements = []
        self.log = None
        if log_file:
            if os.path.exists(log_file):
                self.measurements = calibration.utils.read_log(log_file, sensor_name)
                self.capture = False
            else:
                self.log = open(log_file, "w")
                self.capture = True
        else:
            self.capture = True

        if self.capture:
            self.s = communication.SerialCommunication(
                        transport.Transport(check_crc=True, debug=False),
                        self.m,
                        wasp.transport.TransportHeaderFooter(acid=wasp.ACID_GROUNDSTATION))
            self.s.configure_connection(serial_port=port,serial_speed=57600,serial_timeout=1)
            self.s.connect("message-received", self._on_message_received)
            self.s.connect("uav-connected", self._on_uav_connected)

    def _on_message_received(self, comm, msg, header, payload):
        if msg == self.msg:
            x,y,z = msg.unpack_values(payload)
            if self.log:
                self.log.write("%s %d %d %d\n" % (msg.name,x,y,z))
                self.measurements.append( (float(x),float(y),float(z)) )
            print ".",

    def _request_message(self):
        self.s.send_message(
                self.m.get_message_by_name("REQUEST_TELEMETRY"),
                (self.msg.id, FREQ))
        return False

    def _on_uav_connected(self, comm, connected):
        if connected:
            gobject.timeout_add(1000, self._request_message)
        else:
            self.loop.quit()
            raise SystemExit("Not Connected")

    def _rotate_state_machine(self):
        try:
            self.state += 1
            print self.STATES[self.state]
            return True
        except IndexError:
            self.loop.quit()
            return False

    def collect(self):
        if self.capture:
            self.s.connect_to_uav()
            gobject.timeout_add(STEP_DELAY*1000, self._rotate_state_machine)
            self.loop.run()
            if self.log:
                self.log.close()
            self.measurements = calibration.utils.read_list(self.measurements)

        return self.measurements

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "..", "onboard", "config", "messages.xml")

    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="messages xml file", metavar="FILE")
    parser.add_option("-p", "--port",
                    default="/dev/ttyUSB0",
                    help="Serial port")
    parser.add_option("-l", "--log-file",
                    help="log file for analysis. "\
                    "If it exists it will be used. "\
                    "If it does not exist it will be created. "\
                    "If not supplied the data will be captured directly "\
                    "from the UAV for analysis", metavar="FILE")
    parser.add_option("-s", "--sensor", choices=calibration.SENSORS,
                    help="sensor to calibrate",
                    metavar="[%s]" % ",".join(calibration.SENSORS))


    options, args = parser.parse_args()

    if not options.sensor:
        parser.error("must supply sensor")

    logger = IMULogger(options.port, options.messages, options.sensor, options.log_file)
    measurements = logger.collect()
    calibration.calibrate_sensor(options.sensor, measurements, True)

