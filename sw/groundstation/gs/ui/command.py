import logging
import gtk

import gs.ui
import gs.config as config
import wasp.ui.treeview as treeview
import wasp.fms as fms

LOG = logging.getLogger("settings")

class CommandController(gs.ui.GtkBuilderWidget):

    def __init__(self, source, messagesfile):
        gs.ui.GtkBuilderWidget.__init__(self, "command.ui")

        self._source = source
        self._command_manager = fms.CommandManager(source.communication)

        self.widget = self.get_resource("hbox")

        ts = treeview.MessageTreeStore()
        for m in [i for i in messagesfile.get_messages() if i.is_command]:
            ts.add_message(m)

        self._tv = treeview.MessageTreeView(ts)
        self.get_resource("commands_sw").add(self._tv)

        self.get_resource("command_send_button").connect("clicked", self._send_command)

    def _on_setting(self, msg, header, payload):
        id_, type_, val = msg.unpack_values(payload)
        LOG.debug("Got setting: %d %s" % (id_, val))
        self._sm.update_setting_value(id_, val)

    def _command_ok_response(self):
        LOG.debug("COMMAND OK")

    def _command_fail_response(self, error_code):
        LOG.debug("COMMAND FAIL: %s" % error_code)

    def _send_command(self, btn):
        msg,vals = self._tv.get_selected_message_and_values()
        if msg:
            LOG.info("Sending Command: %s %s" % (msg,vals))
            self._command_manager.send_command(msg, vals, self._command_ok_response, self._command_fail_response)

