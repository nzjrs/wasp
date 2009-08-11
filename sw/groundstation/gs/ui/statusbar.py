import gobject
import gtk

import gs.ui
import gs.ui.indicators as indicators

class StatusBar(gtk.Statusbar):
    def __init__(self, source):
        gtk.Statusbar.__init__(self)

        hb = gtk.HBox()

        #connected indicator
        self._c = indicators.ColorLabelBox("C:",
                                red_message="Communication not connected",
                                green_message="Communication connected")
        hb.pack_start(self._c)
        #status indicator
        #self._s = indicators.ColorLabelBox("S:",
        #                        red_message="UAV Error",
        #                        yellow_message="UAV Warning",
        #                        green_message="UAV OK")
        #hb.pack_start(self._s)
        #autopilot indicator
        self._a = indicators.ColorLabelBox("A:",
                                red_message="Autopilot disabled",
                                green_message="Autopilot enabled")
        hb.pack_start(self._a)
        #manual indicator
        self._m = indicators.ColorLabelBox("M:",
                                red_message="Manual control disabled",
                                green_message="Manual control enabled")
        hb.pack_start(self._m)

        #msgs/second        
        self._ms = gs.ui.make_label("MSG/S: ?", 10)
        hb.pack_start(self._ms, False, False)
        #ping time
        self._pt = gs.ui.make_label("PING: ?", 12)
        hb.pack_start(self._pt, False, False)
        #GPS LLA
        self._gps_coords = gs.ui.make_label("GPS: +180.0000 N, +180.0000 E")
        hb.pack_start(self._gps_coords, False, False)
        #debug
        self._debug = indicators.ColorLabelBox(text="", fade=True)
        self._debug.set_blank()

        hb.pack_start(self._debug, True, True)
       
        self.pack_start(hb, False, False)
        self.reorder_child(hb, 0)

        source.serial.connect("serial-connected", self._on_serial_connected)

        source.register_interest(self._on_gps, 0, "GPS_LLH")
        source.register_interest(self._on_debug, 0, "DEBUG")

        gobject.timeout_add_seconds(1, self._check_messages_per_second, source)

    def _on_serial_connected(self, serial, connected):
        if connected:
            self._c.set_green()
            self._c.set_tooltip_text("")
        else:
            self._c.set_red()
            self._c.set_tooltip_text("Communication disconnected")

    def _check_messages_per_second(self, source):
        self._ms.set_text("MSG/S: %.1f" % source.get_messages_per_second())
        self._pt.set_text("PING: %.1f ms" %  source.get_ping_time())
        return True

    def _on_debug(self, msg, payload):
        value, = msg.unpack_values(payload)
        self._debug.set_text("DEBUG: %d" % value)
        self._debug.set_green()

    def _on_gps(self, msg, payload):
        fix,sv,lat,lon,hsl = msg.unpack_values(payload)

        lat = lat/1e7
        lon = lon/1e7

        self._gps_coords.set_text("GPS: %.4f %s, %.4f %s" % (lat,"N",lon,"E"))



