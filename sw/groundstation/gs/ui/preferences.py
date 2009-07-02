import gtk
import logging

LOG = logging.getLogger('preferences')
class PreferencesWindow:

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
                if idx >= 0:
                    text = widget.get_model()[idx][0]
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
                    for i in range(0, len(mod)):
                        if mod[i][0] == val:
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

