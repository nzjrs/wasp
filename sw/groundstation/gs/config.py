import logging
import ConfigParser

import gtk

LOG = logging.getLogger('config')

class ConfigurableIface:
    """
    A class to make storing persistant configutation information, and generating
    configuration dialogs much easier. For example, plugins may derive from
    this class.

    Derived objects may either call :func:`gs.config.ConfigurableIface.autobind_config` or 
    :func:`gs.config.ConfigurableIface.update_config_from_state` 
    and :func:`gs.config.ConfigurableIface.update_state_from_config` at 
    the appropriate times. :func:`gs.config.ConfigurableIface.get_preference_widgets`
    may be overriden if the derived object also wishes to install a tab in 
    the GUI preferences window.
    """

    #: The section name in the config.ini file the derived class settings are
    #: stored in. This must not be *None*
    CONFIG_SECTION = None

    def __init__(self, config):
        """
        :param config: a :class:`gs.config.Config` object
        """
        assert(self.CONFIG_SECTION)
        self._config = config
        self._autobind_keys = []
        self._autobind_update_state_cb = None
        self._autobind_update_config_cb = None

    def config_get(self, key, default):
        """ Returns a configuration value """
        return self._config.get(key, default, section=self.CONFIG_SECTION)

    def config_set(self, key, value):
        """ Saves a configuration value in the objects setcion """
        self._config.set(key, value, section=self.CONFIG_SECTION)

    def config_delete_keys_in_section(self):
        """ Deletes all configuration values in the objects secion """
        self._config.delete_keys_in_section(section=self.CONFIG_SECTION)

    def autobind_config(self, *keys, **kwargs):
        """
        Autobinds configuration variables of the supplied names to
        instance properties. It saves you having to implement
        update_{state,config}_from_{config,state} functions.
        A default value for the configutaion variable
        must be present as a class property. For example ::

            autobind_config("foo")

            implies the following;
                self._foo
                    Contains the value of the config called foo
                self.DEFAULT_FOO
                    Must contain the default value of foo

        You can also pass two callbacks to this function, update_state_cb and
        update_config_cb - these are callbacks that will get called after the
        default update_state_from_config and update_config_from_state is
        called.
        """
        self._autobind_keys = keys
        for key in self._autobind_keys:
            default = getattr(self, "DEFAULT_%s" % key.upper())
            val = self.config_get(key, default)
            setattr(self, "_%s" % key, val)

        self._autobind_update_state_cb = kwargs.get("update_state_cb", None)
        self._autobind_update_config_cb = kwargs.get("update_config_cb", None)

    def update_state_from_config(self):
        """
        Function that should update the widget state from values stored in
        the config file. Called at initialization and after every time the user
        opens the preferences dialog
        """
        for key in self._autobind_keys:
            default = getattr(self, "DEFAULT_%s" % key.upper())
            setattr(self, "_%s" % key, self.config_get(key, default))

        if self._autobind_update_state_cb:
            try:
                self._autobind_update_state_cb()
            except:
                LOG.warning("Error calling update_state cb", exc_info=True)

    def update_config_from_state(self):
        """
        Funtion that should write the widget state to the config file. Called
        at exit and after every time the user opens the preferences dialog
        """
        for key in self._autobind_keys:
            val = getattr(self, "_%s" % key)
            self.config_set(key, val)

        if self._autobind_update_config_cb:
            try:
                self._autobind_update_config_cb()
            except:
                LOG.warning("Error calling update_config cb", exc_info=True)

    def get_preference_widgets(self):
        """
        You are encouraged to use the **build_foo** functions
        in here to build the GUI.

        :returns: a 3-tuple containg; the page name, the toplevel widget to be packed, and the configurable widgets. 
        """
        return None, None, []

    def build_sizegroup(self):
        """ Returns a *gtk.SizeGroup* """
        return gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

    def _add_sizegroup(self, lbl, **kwargs):
        sg = kwargs.get("sg")
        if sg:
            sg.add_widget(lbl)

    def build_label(self, label, widget, **kwargs):
        """
        Returns a *gtk.HBox* containing a label and the supplied widget
        :param sg: an optional *gtk.SizeGroup* to ensure the label is the same size
        """
        b = gtk.HBox(spacing=10)

        lbl = gtk.Label(label)
        lbl.set_alignment(0, 0.5)

        b.pack_start(lbl, False, False)
        b.pack_start(widget, True, True)

        self._add_sizegroup(lbl, **kwargs)

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

    def build_combo(self, name, *options, **kwargs):
        """
        Returns a *gtk.ComboBox* with the supplied options
        :param name: the config name 
        :param options: a list of strings
        """
        model = gtk.ListStore(str)
        for o in options:
            model.append((o,))
        widget = self._build_combo_widget(name, model)
        self._add_sizegroup(widget, **kwargs)
        return widget

    def build_combo_with_model(self, name, *options, **kwargs):
        """
        Returns a *gtk.ComboBox* with the supplied options
        :param name: the config name
        :param options: a list of 2-tuples containing strings, e.g.
                        (the name to be shown, the value stored)
        """
        model = gtk.ListStore(str, str)
        for n,o in options:
            model.append((n,o))
        widget = self._build_combo_widget(name, model)
        widget.set_data("MODEL_DATA_INDEX", 1)
        self._add_sizegroup(widget, **kwargs)
        return widget

    def build_entry(self, name, **kwargs):
        """
        Returns a *gtk.Entry*
        :param name: the config name
        """
        section = self.CONFIG_SECTION
        widget = gtk.Entry()
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        self._add_sizegroup(widget, **kwargs)
        return widget

    def build_checkbutton(self, name, **kwargs):
        """
        Returns a *gtk.CheckButton*
        :param name: the config name

        Kwargs:
           label (str): The label to be shown in the CheckButton. If not
           supplied, one is generated from the name automatically
        """
        section = self.CONFIG_SECTION
        label = kwargs.get("label", name.replace("_"," ").title())
        widget = gtk.CheckButton(label=label)
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        self._add_sizegroup(widget, **kwargs)
        return widget

    def build_radio(self, name, item, **kwargs):
        """
        Returns a *gtk.RadioButton*
        :param name: the config name
        :param item: the visible label
        """
        section = self.CONFIG_SECTION
        widget = gtk.RadioButton(label=item)
        widget.set_data("CONFIG_NAME", name)
        widget.set_data("CONFIG_SECTION", section)
        self._add_sizegroup(widget, **kwargs)
        return widget

    def build_hbox(self, *items, **kwargs):
        """
        Returns a *gtk.HBox*
        :param items: items added to the HBox
        """
        hb = gtk.HBox(**kwargs)
        for i in items:
            hb.pack_start(i, False)
        return hb

    def build_radio_group(self, name, *options, **kwargs):
        """
        Returns a group of *gtk.RadioButtons* with choices among the supplied options
        :param name: the config name 
        :param options: a list of strings
        """
        buttons = [self.build_radio(name, i, **kwargs) for i in options]

        #make them part of the same group
        for b in buttons[1:]:
            b.set_group(buttons[0])

        return buttons

    def build_frame(self, name, items, **kwargs):
        """
        Return a *gtk.Frame* of the given name containig the supplied items
        """
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
                    if widget.get_group():
                        if widget.get_label() == val:
                            widget.set_active(True)
                    else:
                        if name == val:
                            widget.set_active(True)
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
        
        self._dlg.set_default_size(400,-1)
        self._dlg.show_all()
        response = 0
        while response == 0:
            response = self._dlg.run()
        self._dlg.hide()

        #save the settings to the config file
        if response == gtk.RESPONSE_ACCEPT:
            self._save_widgets_to_config(config)
            
        return response
