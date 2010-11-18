import gtk
import gobject

import logging
import wasp.fms

LOG = logging.getLogger("ui.control")

class ControlController:

    def __init__(self, source, messages_file, settings_file):
        self._source = source
        self._messages_file = messages_file
        self.widget = gtk.VBox(spacing=5)

        self._control_widget = gtk.VBox(spacing=5)
        self.widget.pack_start(self._control_widget, True, True)
        self.widget.pack_start(gtk.HSeparator(), False, False)
        self._status_widget = gtk.Label("")
        self._status_widget.props.xalign = 0.0
        self._status_widget.props.xpad = 5
        self.widget.pack_start(self._status_widget, False, True)
        gobject.timeout_add(1000/10, self._refresh_label)

        self._fms_control = wasp.fms.ControlManager(source, messages_file, settings_file)

    def _set_label(self, enabled, name=None, sp=None):
        LABEL_TEMPLATE = "<b>FMS Mode:</b> %s\n\t<i>roll:</i>\t\t%s\n\t<i>pitch:</i>\t%s\n\t<i>heading:</i>\t%s\n\t<i>thrust:</i>\t%s"
        if enabled:
            self._status_widget.set_markup(LABEL_TEMPLATE % (
                    name,
                    sp[wasp.fms.ID_ROLL],
                    sp[wasp.fms.ID_PITCH],
                    sp[wasp.fms.ID_HEADING],
                    sp[wasp.fms.ID_THRUST])
            )
        else:
            self._status_widget.set_markup(LABEL_TEMPLATE % ("Disabled","","","",""))

    def _refresh_label(self):
        try:
            name, sp = self._fms_control.get_mode_and_setpoints()
            self._set_label(True, name, sp)
        except TypeError:
            #no fms enalbed
            self._set_label(False)
        return True

    def _on_enabled(self, btn, widget, control_widget):
        enabled = btn.get_active()
        widget.set_sensitive(enabled)
        control_widget.set_control_enabled(enabled, self._fms_control)
        self._fms_control.enable(enabled)

    def add_control_widget(self, name, control_widget):
        #Each control widget is in a frame with a label and nice padding.
        #to the right lies an unlock button that must be clicked to make the
        #widget sensitive
        widget = control_widget.get_ui_widget()
        b = gtk.CheckButton()
        l = gtk.Label("<b>Enable %s</b>" % name)
        l.props.use_markup = True
        h = gtk.HBox()
        h.pack_start(b, False, False)
        h.pack_start(l, True, True)
        f = gtk.Frame()
        f.props.shadow_type = gtk.SHADOW_NONE
        f.props.label_widget = h
        a = gtk.Alignment()
        a.set_padding(5,0,10,0)
        f.add(a)
        b.connect("toggled", self._on_enabled, widget, control_widget)
        hb = gtk.HBox(spacing=5)
        #make widget unsensitive by default
        widget.set_sensitive(False)
        hb.pack_start(widget, True, True)
        a.add(hb)
        f.show_all()
        self._control_widget.pack_start(f, False, True)

class ControlWidgetIface:

    fms_control = None

    def set_control_enabled(self, enabled, fms_control):
        raise NotImplementedError

    def get_ui_widget(self):
        raise NotImplementedError
