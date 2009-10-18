import gtk
import gobject
import os.path
import logging

import gs.ui
import gs.plugin as plugin
import gs.ui.progressbar as progressbar

LOG = logging.getLogger('radiocalibration')

class RadioCalibrator(plugin.Plugin, gs.ui.GtkBuilderWidget):

    CHANNELS = (
        "THROTTLE",
        "RUDDER",
        "AILERON",
        "ELEVATOR",
        "APMODE",
        "SWITCH"
    )

    def __init__(self, conf, source, messages_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "radiocalibration.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        item = gtk.MenuItem("Calibrate Radio")
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("UAV", item)

        self._nchannels = len(self.CHANNELS)
        self._source = source
        self._initialized = []
        self._win = self.get_resource("mainwindow")
        self._win.connect("delete-event", self._window_closed)
        self.get_resource("close_button").connect("clicked", self._on_close)

    def _show_window(self, *args):
        if not self._initialized:
            #fill the models with names of radio channels
            model = gtk.ListStore(str)
            for c in self.CHANNELS:
                model.append((c,))

            for i in range(1,self._nchannels + 1):
                #fill all the comboboxes with one model
                cb = self.get_resource("combobox%d" % i)
                cell = gtk.CellRendererText()
                cb.pack_start(cell, True)
                cb.add_attribute(cell, 'text', 0)
                cb.set_model(model)
                cb.set_active(0)

                #pack a progressbar for each channel
                hb = self.get_resource("pb_box%d" % i)
                pb = progressbar.ProgressBar(range=None, average=5)
                hb.pack_start(pb)

                self._initialized.append((cb, pb))

            #register interest in the PPM messags
            self._source.register_interest(self._on_ppm, 0, "PPM")

        self._win.show_all()

    def _on_ppm(self, msg, payload):
        ppm = msg.unpack_values(payload)
        for i in range(self._nchannels):
            self._initialized[i][1].set_value(ppm[i])

    def _window_closed(self, *args):
        #hide window, don't destroy it
        self._win.hide()
        return True

    def _on_close(self, *args):
        self._win.hide()



