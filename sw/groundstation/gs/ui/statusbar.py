import gobject
import gtk

import gs.ui
import gs.ui.indicators as indicators
import gs.geo as geo
import gs.source as source

class StatusBar(gtk.Statusbar):
    def __init__(self, source):
        gtk.Statusbar.__init__(self)

        hb = gtk.HBox()

        #connected indicator
        self._c = indicators.ColorLabelBox("C:",
                                red_message="Communication not connected",
                                yellow_message="Communication connected, not receiving data",
                                green_message="Communication connected, receiving data")
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
        #GPS LL
        self._gps_coords = gs.ui.make_label("GPS: +???.???? N, +???.???? E")
        hb.pack_start(self._gps_coords, False, False)
        #Altitude
        self._alt = gs.ui.make_label("ALT: ?????.? m")
        hb.pack_start(self._alt, False, False)
        #Distance from home
        self._dist = gs.ui.make_label("DIST: ?????.? m")
        hb.pack_start(self._dist, False, False)
        self._home_lat = None
        self._home_lon = None
        #debug
        self._debug = indicators.ColorLabelBox(text="", fade=True)
        self._debug.set_blank()

        hb.pack_start(self._debug, True, True)
       
        self.pack_start(hb, False, False)
        self.reorder_child(hb, 0)

        source.connect("source-connected", self._connected_update_icon)
        source.connect("source-link-status-change", self._connected_update_icon)

        source.register_interest(self._on_gps, 0, "GPS_LLH")
        source.register_interest(self._on_debug, 0, "DEBUG")

        gobject.timeout_add_seconds(1, self._check_messages_per_second, source)

    def _connected_update_icon(self, source, *args):
        status = source.get_status()
        if status == source.STATUS_CONNECTED:
            self._c.set_yellow()
        elif status == source.STATUS_CONNECTED_LINK_OK:
            self._c.set_green()
        elif status == source.STATUS_DISCONNECTED:
            self._c.set_red()
        else:
            LOG.critical("Unknown source status: %s" % status)

    def _check_messages_per_second(self, source):
        self._ms.set_text("MSG/S: %.1f" % source.get_messages_per_second())
        self._pt.set_text("PING: %.1f ms" %  source.get_ping_time())
        return True

    def _on_debug(self, msg, header, payload):
        value, = msg.unpack_values(payload)
        self._debug.set_text("DEBUG: %d" % value)
        self._debug.set_green()

    def _on_gps(self, msg, header, payload):
        fix,sv,lat,lon,hsl,hacc,vacc = msg.unpack_scaled_values(payload)

        if fix:
            self._gps_coords.set_text("GPS: %.4f %s, %.4f %s" % (lat,"N",lon,"E"))

            #convert from mm to m
            hsl = hsl/1000.0
            self._alt.set_text("ALT: %.1f m" % hsl)

            #update distance from home
            if self._home_lat != None and self._home_lon != None:
                dist = geo.crow_flies_distance_two_point(
                            (self._home_lat, self._home_lon),
                            (lat, lon))
                self._dist.set_text("DIST: %.1f m" % dist)


    def mark_home(self, lat, lon):
        self._home_lat = lat
        self._home_lon = lon



