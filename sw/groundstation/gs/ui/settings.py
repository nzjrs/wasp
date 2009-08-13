import logging
import gtk

import gs.ui
import wasp.ui.treeview as treeview

LOG = logging.getLogger("settings")

class _EditSetting(gtk.Frame):
    def __init__(self, setting, source, **msgs):
        gtk.Frame.__init__(self, label=setting.name)
        self.set_border_width(5)
        self._setting = setting
        self._source = source

        alignment = gtk.Alignment(xscale=1.0)
        alignment.set_padding(0,5,0,5)
        self.add(alignment)

        self._box = gtk.HBox(spacing=10)
        alignment.add(self._box)

        #create a slider and a spin entry
        min_, default, max_, step = setting.get_value_adjustment()
        self._adj = gtk.Adjustment(
                    value=float(default),
                    lower=float(min_),
                    upper=float(max_),
                    step_incr=float(step),
                    page_incr=10.0*step)

        slider = gtk.HScale(self._adj)
        spin = gtk.SpinButton(self._adj)

        if type(default) == float:
            slider.set_digits(1)
            spin.set_digits(1)
        else:
            slider.set_digits(0)
            spin.set_digits(0)

        self._getmsg = msgs["get"]
        self._msgs = msgs[setting.type]
        self._spin = spin
        self._box.pack_start(slider,True)
        self._box.pack_start(spin,False)

        #get button
        getbtn = gtk.Button("Get")
        getbtn.connect("clicked", self._on_get_button_clicked)
        self._box.pack_start(getbtn, False)

        #set button
        setbtn = gtk.Button("Set")
        setbtn.connect("clicked", self._on_set_button_clicked)
        self._box.pack_start(setbtn, False)

        if not setting.get:
            getbtn.set_sensitive(False)

        if not setting.set:
            slider.set_sensitive(False)
            spin.set_sensitive(False)
            setbtn.set_sensitive(False)

    def _on_set_button_clicked(self, btn):
        v = self._setting.format_value(self._adj.value)
        LOG.debug("Set setting: %s = %s" % (self._setting.name, v))
        self._source.send_message(
                        self._msgs,
                        (self._setting.id, self._setting.type_enum_value, v))

    def _on_get_button_clicked(self, btn):
        LOG.debug("Get setting: %s" % self._setting.name)
        self._source.send_message(
                        self._getmsg,
                        (self._setting.id,))

    def set_size(self, sizegroup):
        sizegroup.add_widget(self._spin)

class _EditSettingsManager(gtk.ScrolledWindow):
    def __init__(self, source, **msgs):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self._vb = gtk.VBox(spacing=10)
        self._sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        self._settings = {}
        self._source = source
        self._msgs = msgs

        self.add(self._vb)

    def add_setting(self, setting):
        if setting not in self._settings:
            es = _EditSetting(setting, self._source, **self._msgs)
            es.set_size(self._sg)
            es.show_all()
            self._vb.pack_start(es, False, True)
            self._settings[setting] = es

class SettingsController(gs.ui.GtkBuilderWidget):

    MSGS = {0:"No",1:"Yes"}

    def __init__(self, source, settingsfile, messagesfile):
        gs.ui.GtkBuilderWidget.__init__(self, gs.ui.get_ui_file("settings.ui"))

        self._source = source
        self._settingsfile = settingsfile
        self.widget = self.get_resource("hbox")

        #the settings manager controls sending new settings to the craft
        self._sm = _EditSettingsManager(source,
                        get=messagesfile.get_message_by_name("GET_SETTING"),
                        uint8=messagesfile.get_message_by_name("SETTING_UINT8"),
                        float=messagesfile.get_message_by_name("SETTING_FLOAT")
        )
        self.get_resource("setting_right_vbox").pack_start(self._sm, False, True)

        ts = treeview.SettingsTreeStore()
        for s in self._settingsfile.all_settings:
            ts.add_setting(s)

        tv = treeview.SettingsTreeView(ts, show_all=False)

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
        LOG.debug("Got setting")

    def _on_es_clicked(self, btn, _tv):
        setting = _tv.get_selected_setting()
        if setting:
            self._sm.add_setting(setting)

    def _on_selection_changed(self, _ts, _tv):
        self.get_resource("setting_info_hbox").set_sensitive(True)
        edit_btn = self.get_resource("setting_edit_button")

        setting = _tv.get_selected_setting()
        if setting:
            self.get_resource("name_value").set_text(setting.name)
            self.get_resource("value_value").set_text(setting.default_value_string)
            self.get_resource("can_set_value").set_text(self.MSGS[setting.set])
            self.get_resource("can_get_value").set_text(self.MSGS[setting.get])
            self.get_resource("doc_value").set_text(setting.doc)

            if setting.set or setting.get:
                edit_btn.set_sensitive(True)
            else:
                edit_btn.set_sensitive(False)

        else:
            edit_btn.set_sensitive(False)

