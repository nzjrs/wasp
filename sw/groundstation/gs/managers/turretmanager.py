import logging

import gs.config as config
import gs.data as data
import gs.ui.source as source

import libserial.SerialSender

LOG = logging.getLogger('turret')

class TurretManager(libserial.SerialSender.SerialSender, config.ConfigurableIface, source.PeriodicUpdateFromSource):
    CONFIG_SECTION = "TURRET"
    def __init__(self, conf):
        libserial.SerialSender.SerialSender.__init__(self, speed=9600)
        config.ConfigurableIface.__init__(self, conf)
        source.PeriodicUpdateFromSource.__init__(self, freq=2)

        #cache the format string
        self._gpggaString =  "$GPGGA,,%("+data.LAT+")s,%("+data.LAT_HEM+")s,"
        self._gpggaString += "%("+data.LON+")s,%("+data.LON_HEM+")s,1,,,"
        self._gpggaString += "%("+data.ALT+")s,M,,M,,,*75 \r\n"

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

    def update_from_data(self, kwargs):
        """
        Override send because turrent expects things in positive
        southern eastern hemispheres, e.g.
        $GPRMC,031723.000,A,4331.3467,S,17235.0691,E,
        """
        pass
        #myargs = kwargs.copy()

        #if kwargs[data.LAT_HEM] == "S":
        #    myargs[data.LAT_HEM] = kwargs[data.LAT_HEM]
        #    myargs[data.LAT] = kwargs[data.LAT]
        #else:
        #    myargs[data.LAT_HEM] = "S"
        #    myargs[data.LAT] = -1.0*kwargs[data.LAT]

        #if kwargs[data.LON_HEM] == "E":
        #    myargs[data.LON_HEM] = kwargs[data.LON_HEM]
        #    myargs[data.LON] = kwargs[data.LON]
        #else:
        #    myargs[data.LON_HEM] = "E"
        #    myargs[data.LON] = -1.0*kwargs[data.LON]

        #libserial.SerialSender.send(self, **myargs)


