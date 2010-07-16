import logging
import os.path

import gtk
import gs.ui
import gs.plugin as plugin
import gs.config as config
import gs.joystick as joystick
import gs.ui.progressbar as progressbar
import gs.ui.joystick as joystickui
import gs.ui.msgarea as msgarea

import wasp.fms as fms

LOG = logging.getLogger('control.joystick')

class ControlJoystick(plugin.Plugin, config.ConfigurableIface):

    CONFIG_SECTION          = "CONTROL_JOYSTICK"
    DEFAULT_DEVICE          = "/dev/input/js0"
    DEFAULT_AXIS_ROLL       = "0"
    DEFAULT_AXIS_PITCH      = "1"
    DEFAULT_AXIS_HEADING    = "2"
    DEFAULT_AXIS_THRUST     = "3"

    AXIS_ID_ROLL            = 0
    AXIS_ID_PITCH           = 1
    AXIS_ID_HEADING         = 2
    AXIS_ID_THRUST          = 3

    def __init__(self, conf, source, messages_file, groundstation_window):

        if not joystick.list_devices():
            raise plugin.PluginNotSupported("No Joystick (/dev/input/js) devices found")

        config.ConfigurableIface.__init__(self, conf)
        self.autobind_config(
                "device",
                "axis_roll", "axis_pitch", "axis_heading", "axis_thrust",
                update_state_cb=self._on_joystick_device_set)
    
        self.control = fms.ControlManager(source, messages_file)

        self.joystick = None
        self.joystick_id = None

        groundstation_window.add_control_widget(
                "Joystick Control",
                self._build_ui())

    def _on_joystick_device_set(self):
        if self.joystick != None:
            self.joystick.close()
            self.joystick.disconnect(self.joystick_id)

        self.joystick = joystick.CalibratedJoystick(device=self._device)
        self.joystick_id = self.joystick.connect("axis", self._on_joystick_event)

        self.joystick.axis_remap(int(self._axis_roll), self.AXIS_ID_ROLL)
        self.joystick.axis_remap(int(self._axis_pitch), self.AXIS_ID_PITCH)
        self.joystick.axis_remap(int(self._axis_heading), self.AXIS_ID_HEADING)
        self.joystick.axis_remap(int(self._axis_thrust), self.AXIS_ID_THRUST)

        self.jsw.set_joystick(self.joystick)

        LOG.info("Joystick initialized: %s" % self._device)

    def _build_ui(self):
        vb = gtk.VBox()
        self.jsw = joystickui.JoystickWidget(num_axis=4, axis_labels=("R","P","Y","T"), show_range=False)
        vb.pack_start(self.jsw, True, True)
        return vb

    def _on_joystick_event(self, joystick, joystick_axis, joystick_value, init):
        pass
        #try:
        #    label, progress_bar, fms_axis_id = self.progress[ self.axis_channel[joystick_axis] ]
        #    value = gs.scale_to_range(
        #                    joystick_value,
        #                    oldrange=(-32767,32767),
        #                    newrange=(0.0,1.0),
        #                    reverse=self.axis_reverse[joystick_axis])
        #    progress_bar.set_value(value)
        #except KeyError:
        #    #ignored axis
        #    pass

    def get_preference_widgets(self):
        #all following items configuration is saved
        ar = self.build_radio_group("axis_roll", "0","1","2","3","4","5","6","7")
        ap = self.build_radio_group("axis_pitch", "0","1","2","3","4","5","6","7")
        ah = self.build_radio_group("axis_heading", "0","1","2","3","4","5","6","7")
        at = self.build_radio_group("axis_thrust", "0","1","2","3","4","5","6","7")
        es = self.build_combo("device", *joystick.list_devices())

        items = ar + ap + ah + at + [es]

        #the gui looks like
        sg = self.build_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Joystick Device", es, sg=sg),
            self.build_label("Roll Axis", self.build_hbox(*ar), sg=sg),
            self.build_label("Pitch Axis", self.build_hbox(*ap), sg=sg),
            self.build_label("Heading Axis", self.build_hbox(*ah), sg=sg),
            self.build_label("Thrust Axis", self.build_hbox(*at), sg=sg)
        ])

        hb = gtk.HBox(spacing=5)
        hb.pack_start(frame, True, True)

        jsw = joystickui.JoystickWidget(num_axis=8, show_uncalibrated=True, show_range=False)
        jsw.set_joystick(self.joystick)
        hb.pack_start(jsw, False, False)

        #Now add an infobar to show some usage instructions
        info = msgarea.InfoBar(
                    primary_text="Match Joystick Channels to Control Axis",
                    secondary_text="""\
For each axis on the left, select the corresponding joystick axis on the right.
You should move the selected joystick to see which axis it supports""")
        vb = gtk.VBox(spacing=5)
        vb.pack_start(hb, True, True)
        vb.pack_start(info, False, False)

        return "Joystick", vb, items
 
