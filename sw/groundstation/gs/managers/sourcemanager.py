import logging

import gs.config as config
import gs.sources.rand as rand
#from gs.sources.albatross import AlbatrossSocketDataEmitter
#from gs.sources.gps import GPSReceiverDataEmitter

import libserial

LOG = logging.getLogger('groundstation')

class SourceManager(config.ConfigurableIface):
    CONFIG_SECTION = "SOURCE"

    SOURCE_RANDOM = "Random"
    SOURCE_RANDOM_THREADED = "Random Threaded"
    SOURCE_NETWORK = "Network"
    SOURCE_SERIAL = "Serial"
    SOURCE_GPS = "NMEA Gps Receiver"
    NETWORK_HOST = "localhost"
    NETWORK_PORT = "7000"

    def __init__(self, conf):
        config.ConfigurableIface.__init__(self, conf)
        self._kwargs = {}
        self._source = None

    def update_state_from_config(self):
        data_emitter_source = self.config_get("uav_source", self.SOURCE_RANDOM)
        kwargs = {
            "uav_source":data_emitter_source
        }

        if data_emitter_source == self.SOURCE_RANDOM:
            DataEmitterKlass = rand.RandomDataEmitter
        #elif data_emitter_source == self.SOURCE_RANDOM_THREADED:
        #    DataEmitterKlass = RandomThreadedDataEmitter
        #elif data_emitter_source == self.SOURCE_NETWORK:
        #    DataEmitterKlass = AlbatrossSocketDataEmitter
        #    kwargs["host"] = self.config_get("network_host", self.NETWORK_HOST)
        #    kwargs["port"] = self.config_get("network_port", self.NETWORK_PORT)
        #    kwargs["port"] = int(kwargs["port"])
        #elif data_emitter_source == "serial":
        #    pass
        #elif data_emitter_source == "nmea_gps":
        #    DataEmitterKlass = GPSReceiverDataEmitter

        #re-instantiate the data-emitter if anything has changed
        if kwargs != self._kwargs:
            LOG.info("Instantiating data-emitter: %s" % data_emitter_source)
            #stop the old one
            if self._source:
                self._source.quit()
            self._source = DataEmitterKlass(**kwargs)
            self._kwargs = kwargs

    def update_config_from_state(self):
        self.config_set("uav_source",   self._kwargs.get("uav_source", self.SOURCE_RANDOM))
        self.config_set("network_host", self._kwargs.get("host", self.NETWORK_HOST))
        self.config_set("network_port", self._kwargs.get("port", self.NETWORK_PORT))

    def get_preference_widgets(self):
        ran_btn = self.build_radio("uav_source", self.SOURCE_RANDOM)
        rant_btn = self.build_radio("uav_source", self.SOURCE_RANDOM_THREADED)
        net_btn = self.build_radio("uav_source", self.SOURCE_NETWORK)
        ser_btn = self.build_radio("uav_source", self.SOURCE_SERIAL)
        gps_btn = self.build_radio("uav_source", self.SOURCE_GPS)

        #make part of same group
        for b in (rant_btn, net_btn, ser_btn, gps_btn):
            b.set_group(ran_btn)

        net_host_ent = self.build_entry("network_host")
        net_port_ent = self.build_entry("network_port")
        ser_port_cb = self.build_combo("serial_port", *libserial.get_ports())
        ser_speed_cb = self.build_combo("serial_speed", *libserial.get_speeds())

        #all following items configuration is saved
        items = [ran_btn, net_btn, ser_btn, gps_btn, net_host_ent, net_port_ent, ser_port_cb, ser_speed_cb]

        #the gui looks like
        sg = self.make_sizegroup()
        frame = self.build_frame(None, [
            ran_btn,
            net_btn,
            self.build_label("Network Host", net_host_ent, sg),
            self.build_label("Network Port", net_port_ent, sg),
            ser_btn,
            self.build_label("Serial Port", ser_port_cb, sg),
            self.build_label("Serial Baud", ser_speed_cb, sg),
            gps_btn
        ])

        return "UAV Data Source", frame, items

    def get_source(self):
        return self._source


