import logging

import gs.config as config

import libserial.SerialSender

LOG = logging.getLogger('turret')

class TurretManager(libserial.SerialSender.SerialSender, config.ConfigurableIface):
    CONFIG_SECTION = "TURRET"
    def __init__(self, conf):
        libserial.SerialSender.SerialSender.__init__(self, speed=9600)
        config.ConfigurableIface.__init__(self, conf)

        #cache the format string
        self._gpggaString =  "$GPGGA,,%(lat)s,%(lat_hem)s,"
        self._gpggaString += "%(lon)s,%(lon_hem)s,1,,,"
        self._gpggaString += "%(alt)s,M,,M,,,*75 \r\n"

        LOG.debug("GGA String: %s" % self._gpggaString)

    def update_state_from_config(self):
        p = self.config_get("serial_port", "")
        LOG.debug("Serial port: %s" % p)
        if p:
            self.connect(port=p)

    def get_preference_widgets(self):
        items = [
            self.build_combo("serial_port", *libserial.get_ports()),
        ]
        frame = self.build_frame("Turret", items)

        return "Turret", frame, items

    def get_data(self):
        return self._gpggaString

