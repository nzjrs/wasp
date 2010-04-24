import subprocess
import logging

import gs.plugin as plugin
import gs.config as config

LOG = logging.getLogger('speak')

class Speak(plugin.Plugin, config.ConfigurableIface):

    CONFIG_SECTION = "SPEAK"
    DEFAULT_ENABLED = "0"

    def __init__(self, conf, source, messages_file, groundstation_window):
        config.ConfigurableIface.__init__(self, conf)
        self.autobind_config("enabled")
        self.process = None
        source.connect("source-connected", self._source_connected)

    def _speak(self, msg):
        if self._enabled != "1":
            return

        if self.process != None:
            #check and set returncode
            self.process.poll()
            if self.process.returncode == None:
                #espeak hasnt terminated yet
                return

        self.process = subprocess.Popen(
                ["espeak", "\"%s\"" % msg],
                )

    def _source_connected(self, source, *args):
        status = source.get_status()
        if status == source.STATUS_CONNECTED:
            self._speak("connected")
        elif status == source.STATUS_CONNECTED_LINK_OK:
            self._speak("connected ok")
        elif status == source.STATUS_DISCONNECTED:
            self._speak("disconnected")

    def get_preference_widgets(self):
        e = self.build_checkbutton("enabled")
        
        items = [e]
        frame = self.build_frame(None, [
            e,
        ])

        return "Speak", frame, items
