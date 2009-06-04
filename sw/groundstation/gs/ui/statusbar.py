import gtk

import gs.ui
import gs.data as data
import gs.ui.source as source
import gs.ui.indicators as indicators

class StatusBar(gtk.Statusbar, source.PeriodicUpdateFromSource):
    def __init__(self):
        gtk.Statusbar.__init__(self)
        source.PeriodicUpdateFromSource.__init__(self, freq=2)

        hb = gtk.HBox()

        #connected indicator
        self._c = indicators.ColorLabelBox("C:")
        hb.pack_start(self._c)
        #status (error, warning, ok) indicator
        self._s = indicators.ColorLabelBox("S:")
        hb.pack_start(self._s)
        #auto indicator
        self._a = indicators.ColorLabelBox("A:")
        hb.pack_start(self._a)
        #manual indicator
        self._m = indicators.ColorLabelBox("M:")
        hb.pack_start(self._m)

        self._gps_coords = gs.ui.make_label("GPS: +180.0000 N, +180.0000 E")
        hb.pack_start(self._gps_coords, False, False)

        self._ms = gs.ui.make_label("MSG/S: 0", 15)
        hb.pack_start(self._ms, False, False)
        
        self.pack_start(hb, False, False)
        self.reorder_child(hb, 0)

    def update_from_data(self, source):
        la, lah, lo, loh, msgs, connected, err, warn = source.get_data(
                data.LAT,data.LAT_HEM,data.LON,data.LON_HEM,
                data.MSG_PER_SEC,
                data.IS_CONNECTED,
                data.ERROR,data.WARNING)
        self._gps_coords.set_text("GPS: %.4f %s, %.4f %s" % (la,lah,lo,loh))
        self._ms.set_text("MSG/S: %.1f" % msgs)

        #check for error or warning
        if connected:
            self._c.set_green()
        else:
            self._c.set_red()

        if err:
            self._s.set_red()
        elif warn:
            self._s.set_yellow()
        else:
            self._s.set_green()


