import os.path
import logging

import gtk
import gs.ui
import gs.plugin as plugin
import gs.ui.control as control
import wasp.fms as fms

LOG = logging.getLogger('control.manual')

class ControlManual(plugin.Plugin, gs.ui.GtkBuilderWidget, control.ControlWidgetIface):

    BUTTON_MAPS = {
        "thrust_up":(fms.ID_THRUST, 5),
        "thrust_down":(fms.ID_THRUST, -5),
        "pitch_up":(fms.ID_PITCH, 5),
        "pitch_down":(fms.ID_PITCH, -5),
        "roll_right":(fms.ID_ROLL, 5),
        "roll_left":(fms.ID_ROLL, -5),
    }


    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "control_manual.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self.ui = self.get_resource("table1")
        groundstation_window.add_control_widget(
                "Manual Control",
                self)

        for b in self.BUTTON_MAPS:
            id_,delta = self.BUTTON_MAPS[b]
            self.get_resource(b).connect("clicked", self._button_clicked, id_, delta)

        LOG.info("Manual Control initialized")

    def _button_clicked(self, b, id_, delta):
        if self.fms_control:
            self.fms_control.adjust_attitude(id_, delta)

    def set_control_enabled(self, enabled, fms_control):
        LOG.debug("fms_control: %s" % fms_control)
        self.fms_control = fms_control

    def get_ui_widget(self):
        return self.ui
