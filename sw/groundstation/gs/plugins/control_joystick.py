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
    DEFAULT_BUTTON_MOTOR_START  = "2"
    DEFAULT_BUTTON_MOTOR_STOP   = "3"

    AXIS_ID_ROLL            = fms.ID_ROLL
    AXIS_ID_PITCH           = fms.ID_PITCH
    AXIS_ID_HEADING         = fms.ID_HEADING
    AXIS_ID_THRUST          = fms.ID_THRUST
    MAX_AXIS_ID             = fms.ID_THRUST + 1

    #limit joystick authority to less than full command range
    RANGE_ATTITUDE_ROLL     = map(lambda x: x * 0.5, fms.RANGE_ATTITUDE[fms.ID_ROLL])
    RANGE_ATTITUDE_PITCH    = map(lambda x: x * 0.5, fms.RANGE_ATTITUDE[fms.ID_PITCH])
    RANGE_ATTITUDE_HEADING  = map(lambda x: x * 0.5, fms.RANGE_ATTITUDE[fms.ID_HEADING])
    RANGE_ATTITUDE_THRUST   = fms.RANGE_ATTITUDE[fms.ID_THRUST]

    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):

        if not joystick.list_devices():
            raise plugin.PluginNotSupported("No Joystick (/dev/input/js) devices found")

        config.ConfigurableIface.__init__(self, conf)
        self.autobind_config(
                "device",
                "axis_roll", "axis_pitch", "axis_heading", "axis_thrust",
                "reverse_roll", "reverse_pitch", "reverse_heading", "reverse_thrust",
                "button_motor_start", "button_motor_stop",
                update_state_cb=self._on_joystick_device_set)

        self.joystick = None
        self.joystick_axis_id = None

        self.ui = gtk.VBox()
        self.jsw = joystickui.JoystickWidget(num_axis=4, axis_labels=("R","P","Y","T"), show_range=False)
        self.ui.pack_start(self.jsw, True, True)

        groundstation_window.add_control_widget(
                "Joystick Control",
                self)

        #YUCK, this breaks abstraction a bit, as commandcontroller is a UI widget...
        self.command_controller = groundstation_window.commandcontroller
        self.start_motors_message = messages_file.get_message_by_name("MOTORS_START")
        self.stop_motors_message = messages_file.get_message_by_name("MOTORS_STOP")

        self._attitude_vals = [0.0] * self.MAX_AXIS_ID

    def _on_joystick_device_set(self):
        if self.joystick != None:
            self.joystick.close()
            self.joystick.disconnect(self.joystick_axis_id)
            self.joystick.disconnect(self.joystick_button_id)

        self.joystick = joystick.CalibratedJoystick(device=self._device)
        self.joystick_axis_id = self.joystick.connect("axis", self._on_joystick_event)
        self.joystick_button_id = self.joystick.connect("button", self._on_joystick_button)

        self.joystick.axis_remap(int(self._axis_roll), self.AXIS_ID_ROLL)
        self.joystick.axis_remap(int(self._axis_pitch), self.AXIS_ID_PITCH)
        self.joystick.axis_remap(int(self._axis_heading), self.AXIS_ID_HEADING)
        self.joystick.axis_remap(int(self._axis_thrust), self.AXIS_ID_THRUST)

        self.joystick.axis_reverse(int(self._axis_roll), self._reverse_roll == "1")
        self.joystick.axis_reverse(int(self._axis_pitch), self._reverse_pitch == "1")
        self.joystick.axis_reverse(int(self._axis_heading), self._reverse_heading == "1")
        self.joystick.axis_reverse(int(self._axis_thrust), self._reverse_thrust == "1")

        self.jsw.set_joystick(self.joystick)

        LOG.info("Joystick initialized: %s" % self._device)

    def _on_joystick_button(self, joystick, button_num, button_value, init):
        if self.fms_control and button_value:
            if button_num == int(self._button_motor_start):
                self.command_controller.send_command(self.start_motors_message, ())
            elif button_num == int(self._button_motor_stop):
                self.command_controller.send_command(self.stop_motors_message, ())

    def _on_joystick_event(self, joystick, joystick_axis, joystick_value, init):
        if self.fms_control:
            if joystick_axis < self.MAX_AXIS_ID:
                #scale to the range expected by the attitude message
                if joystick_axis == self.AXIS_ID_THRUST:
                    val = gs.scale_to_range(joystick_value,
                                            oldrange=(-32767,32767),
                                            newrange=self.RANGE_ATTITUDE_THRUST)
                elif joystick_axis == self.AXIS_ID_ROLL:
                    val = gs.scale_to_range(joystick_value,
                                            oldrange=(-32767,32767),
                                            newrange=self.RANGE_ATTITUDE_ROLL)
                elif joystick_axis == self.AXIS_ID_PITCH:
                    val = gs.scale_to_range(joystick_value,
                                            oldrange=(-32767,32767),
                                            newrange=self.RANGE_ATTITUDE_PITCH)
                elif joystick_axis == self.AXIS_ID_HEADING:
                    val = gs.scale_to_range(joystick_value,
                                            oldrange=(-32767,32767),
                                            newrange=self.RANGE_ATTITUDE_HEADING)


                self._attitude_vals[joystick_axis] = float(val)
                self.fms_control.set_attitude(*self._attitude_vals)

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
        bi = self.build_radio_group("button_motor_start", "0","1","2","3","4","5","6","7")
        bo = self.build_radio_group("button_motor_stop", "0","1","2","3","4","5","6","7")
        es = self.build_combo("device", *joystick.list_devices())

        items = ar + ap + ah + at + [es, rr, rp, rh, rt] + bi + bo

        #the gui looks like
        sg = self.build_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Joystick Device", es, sg=sg),
            self.build_label("Roll Axis", self.build_hbox(rr, *ar), sg=sg),
            self.build_label("Pitch Axis", self.build_hbox(rp, *ap), sg=sg),
            self.build_label("Heading Axis", self.build_hbox(rh, *ah), sg=sg),
            self.build_label("Thrust Axis", self.build_hbox(rt, *at), sg=sg),
            self.build_label("Motor Start Button", self.build_hbox(*bi), sg=sg),
            self.build_label("Motor Stop Button", self.build_hbox(*bo), sg=sg)
        ])

        hb = gtk.HBox(spacing=5)
        hb.pack_start(frame, True, True)

        jsw = joystickui.JoystickWidget(num_axis=8, show_uncalibrated=True, show_buttons=True, show_range=False)
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

 
