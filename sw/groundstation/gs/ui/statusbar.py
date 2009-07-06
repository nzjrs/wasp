import gobject
import gtk

import gs.ui
import gs.ui.indicators as indicators

class StatusBar(gtk.Statusbar):
    def __init__(self, source):
        gtk.Statusbar.__init__(self)

        hb = gtk.HBox()

        #connected indicator
        self._c = indicators.ColorLabelBox("C:")
        hb.pack_start(self._c)
        #status indicator
        self._s = indicators.ColorLabelBox("S:")
        hb.pack_start(self._s)
        #autopilot indicator
        self._a = indicators.ColorLabelBox("A:")
        hb.pack_start(self._a)
        #manual indicator
        self._m = indicators.ColorLabelBox("M:")
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
       
        self.pack_start(hb, False, False)
        self.reorder_child(hb, 0)

        source.register_interest(self._on_gps, 0, "GPS_LLH")

        gobject.timeout_add_seconds(1, self._check_messages_per_second, source)

    def _check_messages_per_second(self, source):
        self._ms.set_text("MSG/S: %.1f" % source.get_messages_per_second())
        self._pt.set_text("PING: %.1f ms" %  source.get_ping_time())
        return True

    def _on_gps(self, msg, payload):
        fix,sv,lat,lon,hsl = msg.unpack_values(payload)

        lat = lat/1e7
        lon = lon/1e7

        self._gps_coords.set_text("GPS: %.4f %s, %.4f %s" % (lat,"N",lon,"E"))

    def update_connected_indicator(self, connected):
        if connected:
            self._c.set_green()
        else:
            self._c.set_red()


