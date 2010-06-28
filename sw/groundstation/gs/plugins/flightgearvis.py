import gtk
import os.path
import logging
import subprocess

import gs.ui
import gs.plugin as plugin
import wasp.sim as sim

LOG = logging.getLogger('fgvis')

class FlightGearVis(plugin.Plugin):

    def __init__(self, conf, source, messages_file, groundstation_window):
        if not gs.utils.program_installed(sim.EXECUTABLE):
            raise plugin.PluginNotSupported("%s not installed" % sim.EXECUTABLE)

        pb = gs.ui.get_icon_pixbuf("world.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Show Flight in FlightGear")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._start_fgfs)
        groundstation_window.add_menu_item("Window", item)

    def _start_fgfs(self, *args):
        pass
