import logging
import ConfigParser

import gtk
import gobject

LOG = logging.getLogger('config')

class ConfigurableIface:

    def __init__(self, config):
        self._config = config

    def config_get(self, key, default):
        return self._config.get(key, default, section=self.CONFIG_SECTION)

    def config_set(self, key, value, section="DEFAULT"):
        self._config.set(key, value, section=self.CONFIG_SECTION)

    def config_delete_keys_in_section(self):
        self._config.delete_keys_in_section(section=self.CONFIG_SECTION)

    def update_state_from_config(self):
        pass

    def update_config_from_state(self):
        pass

    def get_preference_widgets(self):
        """
        Returns the page name, the toplevel widget to be packed, and the 
        configurable widgets
        """
        return None, None, []

    def make_sizegroup(self):
        return gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

    def build_label(self, label, widget, sg=None):
        b = gtk.HBox(spacing=5)

        lbl = gtk.Label(label)
        lbl.set_alignment(0, 0.5)

        b.pack_start(lbl)
        b.pack_start(widget)

        if sg:
            sg.add_widget(lbl)

        return b

    def _build_combo_widget(self, name, model):
        section = self.CONFIG_SECTION
        widget = gtk.ComboBox(model)

        cell = gtk.CellRendererText()
        widget.pack_start(cell, True)
        widget.add_attribute(cell, 'text', 0)

        widget.set_data("MODEL_DATA_INDEX", 0)
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)

        return widget

    def build_combo(self, name, *options):
        model = gtk.ListStore(str)
        for o in options:
            model.append((o,))
        return self._build_combo_widget(name, model)

    def build_combo_with_model(self, name, *options):
        model = gtk.ListStore(str, str)
        for n,o in options:
            model.append((n,o))
        widget = self._build_combo_widget(name, model)
        widget.set_data("MODEL_DATA_INDEX", 1)
        return widget

    def build_entry(self, name):
        section = self.CONFIG_SECTION
        widget = gtk.Entry()
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        return widget

    def build_checkbutton(self, name):
        section = self.CONFIG_SECTION
        widget = gtk.CheckButton(label=name.replace("_"," "))
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        return widget

    def build_radio(self, name, item):
        button = gtk.RadioButton(label=item)
        section = self.CONFIG_SECTION
        button.set_data("CONFIG_NAME", name)
        button.set_data("CONFIG_SECTION", section)
        return button

    def build_radio_group(self, name, *items):
        section = self.CONFIG_SECTION
        buttons = [self.build_radio(name, i) for i in items]

        #make them part of the same group
        for b in buttons[1:]:
            b.set_group(buttons[0])

        return buttons

    def build_frame(self, name, items):
        f = gtk.Frame(name)
        f.set_shadow_type(gtk.SHADOW_NONE)

        if len(items) == 1:
            f.add(items[0])
        else:
            box = gtk.VBox(spacing=5)
            for i in items:
                box.pack_start(i, False, False)
            f.add(box)

        return f

class Config:

    def __init__(self, filename):
        self._filePath = filename
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._filePath)

        LOG.info("Restored config from %s" % filename)

    def get(self, key, default, section="DEFAULT"):
        try:
            value = self._config.get(section,key)
            if value == "":
                value = None
            return value
        except ConfigParser.NoOptionError:
            return default
        except ConfigParser.NoSectionError:
            return default

    def get_keys_in_section(self, section="DEFAULT"):
        try:
            return [i[0] for i in self._config.items(section)]
        except ConfigParser.NoSectionError:
            return []

    def get_sections(self):
        return self._config.sections()

    def delete_keys_in_section(self, section="DEFAULT"):
        for k in self.get_keys_in_section(section):
            self._config.remove_option(section, k)

    def set(self, key, value, section="DEFAULT"):
        if value == None:
            value = ""
        try:
            self._config.set(section, key, value)
        except ConfigParser.NoSectionError:
            self._config.add_section(section)
            self._config.set(section, key, value)

    def save(self):
        fp = open(self._filePath, 'w')
        self._config.write(fp)
        fp.close()

class ConfigWindow:

    def __init__(self, window, configurable):
        self._dlg = gtk.Dialog(
                        "Preferences",
                        window,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                        gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self._nb = gtk.Notebook()
        self._dlg.vbox.pack_start(self._nb)
        self._configurable_widgets = []

        LOG.info("Building preferences window from configurable widgets")

        pages = {}
        for c in configurable:
            if c:
                page, widget, configurable_widgets = c.get_preference_widgets()

                if page and widget:
                    if page in pages:
                        #add to existing page VBox
                        pages[page].pack_start(widget, False, False)
                    else:
                        #create new page
                        box = gtk.VBox()
                        box.pack_start(widget, False, False)
                        self._nb.append_page(box, tab_label=gtk.Label(page))
                        pages[page] = box

                    #save those widgets who are backed by config settings
                    self._configurable_widgets += configurable_widgets

    def _save_widgets_to_config(self, config):
        LOG.info("Saving preferences to config file")
        for widget in self._configurable_widgets:
            name = widget.get_data("CONFIG_NAME")
            section = widget.get_data("CONFIG_SECTION")

            if type(widget) == gtk.Entry:
                config.set(name, widget.get_text(), section)
            elif type(widget) == gtk.ComboBox:
                idx = widget.get_active()
                model_idx = widget.get_data("MODEL_DATA_INDEX")
                if idx >= 0:
                    text = widget.get_model()[idx][model_idx]
                else:
                    text = ""
                config.set(name, text, section)
            elif type(widget) == gtk.RadioButton:
                if widget.get_active():
                    config.set(name, widget.props.label, section)
            elif type(widget) == gtk.CheckButton:
                if widget.get_active():
                    config.set(name, "1", section)
                else:
                    config.set(name, "0", section)
            else:
                LOG.critical("Unknown preference widget: %s" % widget)

    def _load_widgets_from_config(self, config):
        for widget in self._configurable_widgets:
            name = widget.get_data("CONFIG_NAME")
            section = widget.get_data("CONFIG_SECTION")
            val = config.get(name, default=None, section=section)
            if val != None:
                if type(widget) == gtk.Entry:
                    widget.set_text(val)
                elif type(widget) == gtk.ComboBox:
                    idx = 0
                    mod = widget.get_model()
                    model_idx = widget.get_data("MODEL_DATA_INDEX")
                    for i in range(0, len(mod)):
                        if mod[i][model_idx] == val:
                            idx = i
                    widget.set_active(idx)
                elif type(widget) == gtk.RadioButton:
                    if name == val:
                        widget.set_active()
                elif type(widget) == gtk.CheckButton:
                    i = int(val)
                    if i == 1:
                        widget.set_active(True)
                    elif i == 0:
                        widget.set_active(False)
                    else:
                        LOG.critical("Unknown value for check config: %s" % val)

    def show(self, config):
        #preload the widgets
        self._load_widgets_from_config(config)

        self._dlg.show_all()
        response = 0
        while response == 0:
            response = self._dlg.run()
        self._dlg.hide()

        #save the settings to the config file
        if response == gtk.RESPONSE_ACCEPT:
            self._save_widgets_to_config(config)
            
        return response
