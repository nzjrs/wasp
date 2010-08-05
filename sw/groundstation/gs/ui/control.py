import gtk
import logging
import wasp.fms

LOG = logging.getLogger("ui.control")

class ControlController:

    def __init__(self, source, messages_file):
        self._source = source
        self._messages_file = messages_file
        self.widget = gtk.VBox(spacing=5)

        self._fms_control = wasp.fms.ControlManager(source, messages_file)

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
        self.widget.pack_start(f, False, True)

class ControlWidgetIface:

    fms_control = None

    def set_control_enabled(self, enabled, fms_control):
        raise NotImplementedError

    def get_ui_widget(self):
        raise NotImplementedError
