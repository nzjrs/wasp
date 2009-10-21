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

        pb = gs.ui.get_icon_pixbuf("radio.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Calibrate Radio")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("UAV", item)

        self._nchannels = len(self.CHANNELS)
        self._source = source
        self._initialized = []
        self._win = self.get_resource("mainwindow")
        self._win.set_icon(pb)
        self._win.set_title("Calibrate Radio")
        self._win.connect("delete-event", gtk.Widget.hide_on_delete)
        self.get_resource("close_button").connect("clicked", self._on_close)
        self.get_resource("save_button").connect("clicked", self._on_save)

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
                pb = progressbar.ProgressBar(range=(10e3,35e3), average=5)
                hb.pack_start(pb)

                self._initialized.append((cb, pb))

            #request PPM messages
            self._source.request_telemetry("PPM", 5)

            #register interest in the PPM messags
            self._source.register_interest(self._on_ppm, 0, "PPM")

        self._win.show_all()

    def _on_ppm(self, msg, payload):
        ppm = msg.unpack_values(payload)
        for i in range(self._nchannels):
            self._initialized[i][1].set_value(ppm[i])

    def _on_save(self, *args):
        #<?xml version="1.0"?>
        #<!DOCTYPE radio SYSTEM "radio.dtd">
        #<radio name="Futaba T6EXAP" data_min="900" data_max="2100" sync_min ="5000" sync_max ="15000">
        # <channel ctl="1" function="ROLL"     max="1109" neutral="1520" min="1936" average="0"/>
        # <channel ctl="2" function="PITCH"    min="1099" neutral="1525" max="1921" average="0"/>
        # <channel ctl="3" function="THROTTLE" min="1930" neutral="1930" max="1108" average="0"/>
        # <channel ctl="4" function="YAW"      min="1940" neutral="1518" max="1116" average="0"/>
        # <channel ctl="5" function="GAIN1"    min="1100" neutral="1500" max="3000" average="1"/>
        # <channel ctl="6" function="MODE"     min="1900" neutral="1500" max="1100" average="1"/>
        #</radio>

        #FIXME: DOCUMENT THIS SOMEWHERE
        PPM_RADIO_SCALE = 15.0

        try:
            name = self.get_resource("name_entry").get_text()

            txt =   '<?xml version="1.0"?>\n'
            txt +=  '<!DOCTYPE radio SYSTEM "radio.dtd">\n'
            txt +=  '<radio name="%s" data_min="900" data_max="2100" sync_min ="5000" sync_max ="15000">\n' % name
            for i in range(1,self._nchannels + 1):
                max_ = self.get_resource("max_entry%d" % i).get_text()
                center_ = self.get_resource("center_entry%d" % i).get_text()
                min_ = self.get_resource("min_entry%d" % i).get_text()
                #convert True/False to 1/0.....
                filter_ = {True:"1",False:"0"}[self.get_resource("filter_cb%d" % i).get_active()]
                txt += '    <channel ctl="%d" function="%s" max="%.0f" neutral="%.0f" min="%.0f" average="%s"/>\n' % (
                            i,
                            self.get_resource("combobox%d" % i).get_active_text(),
                            float(max_)/PPM_RADIO_SCALE,
                            float(center_)/PPM_RADIO_SCALE,
                            float(min_)/PPM_RADIO_SCALE,
                            filter_)
            txt +=  '</radio>'
        except:
            LOG.warn("Error generating xml", exc_info=True)
            txt = None

        if txt:
            path = gs.user_file_path("radio.xml")
            f = open(path,"w")
            f.write(txt)
            f.close()
            gs.ui.message_dialog(
                    "Successfully Generated Radio Calibration",
                    self._win,
                    gtk.MESSAGE_INFO,
                    "The file has been saved to %s" % path)
        else:
            gs.ui.message_dialog(
                    "Error Generating Radio Calibration",
                    self._win,
                    secondary="Check all fields were filled.")

        

    def _on_close(self, *args):
        self._win.hide()

