import gtk
import os.path
import logging

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('fms')

class FMS(plugin.Plugin, gs.ui.GtkBuilderWidget):
    def __init__(self, conf, source, messages_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "fms.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        pb = gs.ui.get_icon_pixbuf("joystick.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Remotely Operate")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("UAV", item)

        self._win = self.get_resource("mainwindow")
        self._win.set_icon(pb)
        self._win.set_title("Remotely Operate")
        self._win.connect("delete-event", gtk.Widget.hide_on_delete)
        self.get_resource("close_button").connect("clicked", self._on_close)

        self._parent_window = groundstation_window.window

    def _show_window(self, *args):
        self._win.set_transient_for(self._parent_window)
        self._win.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self._win.show_all()

    def _on_close(self, *args):
        self._win.hide()
