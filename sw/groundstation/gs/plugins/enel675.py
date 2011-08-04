import gtk
import logging

import wasp
import gs.plugin as plugin

LOG = logging.getLogger('enel675')

class ENEL675Plugin(plugin.Plugin):
    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):

        source.register_interest(self._on_ppm, 0, "PPM")
        source.register_interest(self._on_rc, 0, "RC")

        self._ppm = [0]*6
        self._rc = [0]*6

        self._window = None
        item = gtk.MenuItem("RC Monitor")
        item.connect("activate", self._on_menu_item_clicked)
        groundstation_window.add_menu_item("ENEL675", item)

    def _on_menu_item_clicked(self, *args):
        def _create_label(vb, sg, name):
            hb = gtk.HBox()
            l = gtk.Label(name)
            hb.pack_start(l)
            e = gtk.Entry()
            sg.add_widget(l)
            hb.pack_start(e)
            vb.pack_start(hb)
            return e

        if not self._window:
            self._window = gtk.Window()
            self._window.connect("delete-event", gtk.Widget.hide_on_delete)
            vb = gtk.VBox(spacing=4)
            sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
            for i in range(len(self._ppm)):
                self._ppm[i] = _create_label(vb, sg, "PPM: %d " % (i+1))
            for i in range(len(self._rc)):
                self._rc[i] = _create_label(vb, sg, "RC: %d " % (i+1))
            self._window.add(vb)

        self._window.show_all()

    def _on_ppm(self, msg, header, payload):
        if not self._window: return

        ppm = msg.unpack_values(payload)
        for i in range(len(self._ppm)):
            self._ppm[i].set_text(str(ppm[i]))

    def _on_rc(self, msg, header, payload):
        if not self._window: return

        rc = msg.unpack_values(payload)
        for i in range(len(self._rc)):
            self._rc[i].set_text(str(rc[i]))


