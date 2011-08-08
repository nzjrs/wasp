import logging
import gtk

import gs.ui
import gs.config as config
import wasp.ui.treeview as treeview
import wasp.fms as fms

LOG = logging.getLogger("ui.command")

class CommandController(gs.ui.GtkBuilderWidget):

    def __init__(self, source, messagesfile, settings_file):
        gs.ui.GtkBuilderWidget.__init__(self, "command.ui")

        self._source = source

        self.widget = self.get_resource("hbox")

        ts = treeview.MessageTreeStore()
        for m in [i for i in messagesfile.get_messages() if i.is_command]:
            ts.add_message(m)

        self._tv = treeview.MessageTreeView(ts)
        self.get_resource("commands_sw").add(self._tv)

        self.get_resource("command_send_button").connect("clicked", self._on_send_clicked)

    def _on_send_clicked(self, btn):
        msg,vals = self._tv.get_selected_message_and_values()
        if msg:
            self._source.send_command(msg, vals)

