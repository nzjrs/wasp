import subprocess
import logging

import gs.utils
import gs.plugin as plugin
import gs.config as config

LOG = logging.getLogger('speak')

class Speak(plugin.Plugin, config.ConfigurableIface):

    EXECUTABLE = "espeak"
    CONFIG_SECTION = "SPEAK"

    DEFAULT_ENABLED = "0"
    DEFAULT_ANNOUNCE_LOW_BATTERY = "1"
    DEFAULT_ANNOUNCE_BATTERY_VOLTAGE = "0"
    DEFAULT_ANNOUNCE_TELEMETRY = ""

    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):
        if not gs.utils.program_installed(self.EXECUTABLE):
            raise plugin.PluginNotSupported("%s not installed" % self.EXECUTABLE)

        config.ConfigurableIface.__init__(self, conf)
        self.autobind_config("enabled","announce_low_battery","announce_battery_voltage","announce_telemetry")
        self.process = None

        source.connect("source-connected", self._source_connected)
        source.register_interest(self._on_status, 1, "STATUS")

        try:
            self.telemetry_msg,self.telemetry_field = self._announce_telemetry.split(":")
            self.field_idx = messages_file.get_message_by_name(self.telemetry_msg).get_field_index(self.telemetry_field)
            if self.field_idx >= 0:
                source.register_interest(self._on_msg, 1, self.telemetry_msg)
        except:
            pass

        self.batt_low_value = float(settings_file["BATTERY_CRITICAL_VOLTAGE"].value)
        self.bv = self.batt_low_value

    def _speak(self, msg):
        if self._enabled != "1":
            return

        #low battery messages take priority
        if self._announce_low_battery and self.bv < self.batt_low_value:
            msg = "battery: low"

        if self.process != None:
            #check and set returncode
            self.process.poll()
            if self.process.returncode == None:
                #espeak hasnt terminated yet
                return

        self.process = subprocess.Popen(
                [self.EXECUTABLE, "\"%s\"" % msg],
                )

    def _source_connected(self, source, *args):
        status = source.get_status()
        if status == source.STATUS_CONNECTED:
            self._speak("U.A.V: connected")
        elif status == source.STATUS_CONNECTED_LINK_OK:
            self._speak("U.A.V: connected ok")
        elif status == source.STATUS_DISCONNECTED:
            self._speak("U.A.V: disconnected")

    def _on_msg(self, msg, header, payload):
        val = msg.unpack_printable_values(payload,None)[self.field_idx]
        self._speak("%s message: %s = %s" % (self.telemetry_msg,self.telemetry_field,val))

    def _on_status(self, msg, header, payload):
        rc, gps, self.bv, in_flight, motors_on, autopilot_mode, cpu_usage, fms_on, fms_mode = msg.unpack_values(payload)
        say = []

        #check battery voltage (in decivolts)
        if int(self._announce_battery_voltage):
            say.append("battery: %.1f" % (self.bv/10.0))
        elif self.bv < self.batt_low_value:
            say.append("battery: low")

        #check RC is connected
        if rc != msg.get_field_by_name("rc").interpret_value_from_user_string("OK"):
            say.append("R.C: lost")

        if say:
            self._speak(" ... ".join(say))

    def get_preference_widgets(self):
        e = self.build_entry("announce_telemetry")
        items = [
            self.build_checkbutton("enabled"),
            self.build_checkbutton("announce_low_battery"),
            self.build_checkbutton("announce_battery_voltage"),
            e
        ]
        frame = self.build_frame(None,
                    items+[self.build_label("Announce Message (e.g. GPS_LLH:fix)",e)]
        )

        return "Audio Announcements", frame, items
