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
import gs.ui.control as control

import wasp.fms as fms

LOG = logging.getLogger('control.joystick')

class ControlJoystick(plugin.Plugin, config.ConfigurableIface, control.ControlWidgetIface):

    CONFIG_SECTION          = "CONTROL_JOYSTICK"
    DEFAULT_DEVICE          = "/dev/input/js0"
    DEFAULT_AXIS_ROLL       = "0"
    DEFAULT_AXIS_PITCH      = "1"
    DEFAULT_AXIS_HEADING    = "2"
    DEFAULT_AXIS_THRUST     = "3"
    DEFAULT_REVERSE_ROLL    = "0"
    DEFAULT_REVERSE_PITCH   = "0"
    DEFAULT_REVERSE_HEADING = "0"
    DEFAULT_REVERSE_THRUST  = "0"

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
                "reverse_roll", "reverse_pitch", "reverse_heading", "reverse_thrust",
                update_state_cb=self._on_joystick_device_set)

        self.joystick = None
        self.joystick_id = None

        self.ui = gtk.VBox()
        self.jsw = joystickui.JoystickWidget(num_axis=4, axis_labels=("R","P","Y","T"), show_range=False)
        self.ui.pack_start(self.jsw, True, True)

        groundstation_window.add_control_widget(
                "Joystick Control",
                self)

        self._servo_vals = [0,0,0,0,0,0]

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
        if self._reverse_roll:
            self.joystick.axis_reverse(int(self._axis_roll))
        if self._reverse_pitch:
            self.joystick.axis_reverse(int(self._axis_pitch))
        if self._reverse_heading:
            self.joystick.axis_reverse(int(self._axis_heading))
        if self._reverse_thrust:
            self.joystick.axis_reverse(int(self._axis_thrust))


        self.jsw.set_joystick(self.joystick)

        LOG.info("Joystick initialized: %s" % self._device)

    def _on_joystick_event(self, joystick, joystick_axis, joystick_value, init):
        if self.fms_control:
            self._servo_vals[joystick_axis] = int(gs.scale_to_range(
                                                        joystick_value,
                                                        oldrange=(-32767,32767),
                                                        newrange=(-9600,9600)))
            self.fms_control.set_rc(*self._servo_vals)
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
        rr = self.build_checkbutton("reverse_roll", label="R")
        ap = self.build_radio_group("axis_pitch", "0","1","2","3","4","5","6","7")
        rp = self.build_checkbutton("reverse_pitch", label="R")
        ah = self.build_radio_group("axis_heading", "0","1","2","3","4","5","6","7")
        rh = self.build_checkbutton("reverse_heading", label="R")
        at = self.build_radio_group("axis_thrust", "0","1","2","3","4","5","6","7")
        rt = self.build_checkbutton("reverse_thrust", label="R")
        es = self.build_combo("device", *joystick.list_devices())

        items = ar + ap + ah + at + [es, rr, rp, rh, rt]

        #the gui looks like
        sg = self.build_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Joystick Device", es, sg=sg),
            self.build_label("Roll Axis", self.build_hbox(rr, *ar), sg=sg),
            self.build_label("Pitch Axis", self.build_hbox(rp, *ap), sg=sg),
            self.build_label("Heading Axis", self.build_hbox(rh, *ah), sg=sg),
            self.build_label("Thrust Axis", self.build_hbox(rt, *at), sg=sg)
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
You should move the selected joystick to see which axis it supports. You
can also reverse the axis be selecting the 'R' check-box.""")
        vb = gtk.VBox(spacing=5)
        vb.pack_start(hb, True, True)
        vb.pack_start(info, False, False)

        return "Joystick", vb, items

    def set_control_enabled(self, enabled, fms_control):
        self.fms_control = fms_control

    def get_ui_widget(self):
        return self.ui

 
