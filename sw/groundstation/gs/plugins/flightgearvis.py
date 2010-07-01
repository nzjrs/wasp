import gtk
import gobject
import os.path
import logging
import subprocess

import gs
import gs.plugin as plugin
import wasp
import wasp.sim as sim

LOG = logging.getLogger('fgvis')

class FlightGearVis(plugin.Plugin):

    def __init__(self, conf, source, messages_file, groundstation_window):
        if not gs.utils.program_installed(sim.EXECUTABLE):
            raise plugin.PluginNotSupported("%s not installed" % sim.EXECUTABLE)

        start_item = gtk.MenuItem("Start Visualisation")
        start_item.connect("activate", self._start_fgfs)
        stop_item = gtk.MenuItem("Stop Visualisation")
        stop_item.connect("activate", self._stop_fgfs)
        groundstation_window.add_submenu_item("Window", "FlightGear Simulator", start_item, stop_item)

        source.register_interest(self._on_gps, 0, "GPS_LLH")

        self.fg = sim.FlightGearVisualisation()

        self.lat = wasp.HOME_LAT
        self.lon = wasp.HOME_LON
        self.hsl = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        gobject.timeout_add(1000/sim.VIS_REFRESH_RATE, self._update_fgfs)


    def _start_fgfs(self, *args):
        LOG.info("Starting FlightGear")
        self.fg.start()

    def _stop_fgfs(self, *args):
        LOG.info("Stopping FlightGear")
        self.fg.stop()

    def _update_fgfs(self):
        self.fg.set_attitude_position(
                    lat=self.lat,
                    lon=self.lon,
                    alt=self.hsl,
                    roll=self.roll,
                    pitch=self.pitch,
                    yaw=self.yaw)
        return True

    def _on_gps(self, msg, header, payload):
        fix,sv,self.lat,self.lon,hsl,hacc,vacc = msg.unpack_scaled_values(payload)

        #convert from mm to m
        self.hsl = self.hsl/1000.0
