import logging
import gtk

import gs.ui
import wasp.ui.treeview as treeview

LOG = logging.getLogger("settings")

class SettingsController(gs.ui.GtkBuilderWidget):
    def __init__(self, source, settingsfile, messagesfile):
        gs.ui.GtkBuilderWidget.__init__(self, gs.ui.get_ui_file("settings.ui"))

        self._source = source
        self._settingsfile = settingsfile
        self.widget = self.get_resource("hbox")

        #get the messages we need
        self._getmsg = messagesfile.get_message_by_name("GET_SETTING")

        LOG.debug("testing")

        ts = treeview.SettingsTreeStore()
        for s in self._settingsfile.all_settings:
            ts.add_setting(s)

        tv = treeview.SettingsTreeView(ts, show_all=False)
        btn = self.get_resource("setting_get_button")

        btn.connect(
                "clicked",
                self._on_gs_clicked,
                tv)

        tv.get_selection().connect(
                "changed",
                self._on_selection_changed,
                tv,
                btn)

        btn.set_sensitive(False)
        self.get_resource("setting_left_vbox").pack_start(tv, True, True)

        #listen for settings messages
        source.register_interest(self._on_setting, 0, "SETTING_UINT8")
        source.register_interest(self._on_setting, 0, "SETTING_FLOAT")

    def _on_setting(self, msg, payload):
        LOG.debug("Got settings")

    def _on_gs_clicked(self, btn, _tv):
        setting = _tv.get_selected_setting()
        #send it
        self._source.send_message(self._getmsg, (setting.id,))

    def _on_selection_changed(self, _ts, _tv, _btn):
        setting = _tv.get_selected_setting()
        if setting and setting.get:
            _btn.set_sensitive(True)
        else:
            _btn.set_sensitive(False)

