import os.path
import logging

import gtk
import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('control.manual')

class ControlManual(plugin.Plugin, gs.ui.GtkBuilderWidget):
    def __init__(self, conf, source, messages_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "control_manual.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self.ui = self.get_resource("table1")
        groundstation_window.add_control_widget(
                "Manual Control",
                self)

        LOG.info("Manual Control initialized")

    def set_control_enabled(self, enabled):
        pass

    def get_ui_widget(self):
        return self.ui
