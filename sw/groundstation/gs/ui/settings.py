import logging
import gtk

import gs.ui
import wasp.ui.treeview as treeview

LOG = logging.getLogger("settings")

class _EditSetting(gtk.Frame):
    def __init__(self, setting):
        gtk.Frame.__init__(self, label=setting.name)

        self._setting = setting

        self._vb = gtk.VBox()
        self.add(self._vb)

class _EditSettingsManager(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=10)
        self._settings = {}

    def add_setting(self, setting):
        if setting not in self._settings:
            es = _EditSetting(setting)
            self.pack_start(es, False, True)
            self.show_all()
            self._settings[setting] = es

class SettingsController(gs.ui.GtkBuilderWidget):

    MSGS = {0:"No",1:"Yes"}

    def __init__(self, source, settingsfile, messagesfile):
        gs.ui.GtkBuilderWidget.__init__(self, gs.ui.get_ui_file("settings.ui"))

        self._source = source
        self._settingsfile = settingsfile
        self.widget = self.get_resource("hbox")

        #the settings manager controls sending new settings to the craft
        self._sm = _EditSettingsManager()
        self.get_resource("setting_right_vbox").pack_start(self._sm, False, True)

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
        btn.set_sensitive(False)

        btn = self.get_resource("setting_edit_button")
        btn.connect(
                "clicked",
                self._on_es_clicked,
                tv)
        btn.set_sensitive(False)

        tv.get_selection().connect(
                "changed",
                self._on_selection_changed,
                tv)

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

    def _on_es_clicked(self, btn, _tv):
        setting = _tv.get_selected_setting()
        if setting:
            self._sm.add_setting(setting)
        print "edit", setting

    def _on_selection_changed(self, _ts, _tv):
        self.get_resource("setting_info_hbox").set_sensitive(True)
        set_btn = self.get_resource("setting_get_button")
        edit_btn = self.get_resource("setting_edit_button")

        setting = _tv.get_selected_setting()
        if setting:
            self.get_resource("name_value").set_text(setting.name)
            self.get_resource("value_value").set_text(setting.default_value_string)
            self.get_resource("can_set_value").set_text(self.MSGS[setting.set])
            self.get_resource("can_get_value").set_text(self.MSGS[setting.get])
            if setting.get:
                set_btn.set_sensitive(True)
            else:
                set_btn.set_sensitive(False)

            if setting.set:
                edit_btn.set_sensitive(True)
            else:
                edit_btn.set_sensitive(False)

        else:
            set_btn.set_sensitive(False)
            edit_btn.set_sensitive(False)

