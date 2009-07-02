import ConfigParser
import gtk
import gobject

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

    def build_combo(self, name, *options):
        section = self.CONFIG_SECTION
        model = gtk.ListStore(gobject.TYPE_STRING)
        widget = gtk.ComboBox(model)

        cell = gtk.CellRendererText()
        widget.pack_start(cell, True)
        widget.add_attribute(cell, 'text', 0)

        for o in options:
            model.append((o,))
        widget.set_model(model)

        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        
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


