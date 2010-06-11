import gtk

import gs.plugin as plugin

class AltimeterCalibrate(plugin.Plugin):

    def __init__(self, conf, source, messages_file, groundstation_window):
        item = gtk.MenuItem("Recalibrate Altimeter")
        item.connect("activate", self._send_message, source, messages_file["ALTIMETER_RESET"])
        groundstation_window.add_menu_item("UAV", item)

    def _send_message(self, menuitem, source, msg):
        source.send_message(msg, ())
