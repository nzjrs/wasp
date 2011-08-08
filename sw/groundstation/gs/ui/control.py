import gtk
import gobject

import logging
import wasp.fms

LOG = logging.getLogger("ui.control")

def _make_left_fancy_label(txt, use_markup=True, padding=5):
    lbl = gtk.Label(txt)
    lbl.set_use_markup(use_markup)
    lbl.set_alignment(0.0, 0.5)
    lbl.set_padding(padding, 0)
    return lbl

class _FMSAxisWidget(gtk.HBox):
    """ An enable checkbox, label and value for each FMS axis """
    def __init__(self, sizegroup, name, _id, toggled_cb, enabled=True):
        gtk.HBox.__init__(self)

        cb = gtk.CheckButton()
        cb.set_active(enabled)
        cb.connect("toggled", toggled_cb, _id)
        cb.toggled()
        self.pack_start(cb, False, False)

        lbl = _make_left_fancy_label("<i>%s :</i>" % name)
        sizegroup.add_widget(lbl)
        self.pack_start(lbl, False, False)

        self._lbl = _make_left_fancy_label("", False, 0)
        self.pack_start(self._lbl, True, True)

    def set_axis_value(self, value):
        self._lbl.set_text(str(value))

class ControlController:

    def __init__(self, source, messages_file, settings_file):
        self._source = source
        self._messages_file = messages_file
        self._fms_control = wasp.fms.ControlManager(source, messages_file, settings_file)

        #build the UI
        self.widget = gtk.VBox()

        self._control_widget = gtk.VBox(spacing=5)
        self.widget.pack_start(self._control_widget, True, True)
        self.widget.pack_start(gtk.HSeparator(), False, False)
        self._status_widget = gtk.Label("")
        self._status_widget.props.xalign = 0.0
        self._status_widget.props.xpad = 5
        self.widget.pack_start(self._status_widget, False, True)
        gobject.timeout_add(1000/10, self._refresh_label)

        #FMS mode
        hb = gtk.HBox()
        lbl = _make_left_fancy_label("<b>FMS Mode: </b>")
        hb.pack_start(lbl, False, False)
        self._fms_mode_label = _make_left_fancy_label("", False, 0)
        hb.pack_start(self._fms_mode_label, True, True)
        self.widget.pack_start(hb, False, True)

        #each axis gets a widget that manages its value and enabled state
        sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        self._axis_id_widget_map = {}
        for _id in wasp.fms.ID_LIST_FMS_ATTITUDE:
            widget = _FMSAxisWidget(sg, wasp.fms.ID_NAMES[_id], _id, self._fms_axis_enable_toggled)
            self.widget.pack_start(widget, False, True)
            self._axis_id_widget_map[_id] = widget

    def _fms_axis_enable_toggled(self, btn, _id):
        if btn.props.active:
            self._fms_control.enable_axis(_id)
        else:
            self._fms_control.disable_axis(_id)

    def _update_fms_axis_value_labels(self, enabled, name=None, sp=None):
        if enabled:
            self._fms_mode_label.set_text (name)
            for _id in wasp.fms.ID_LIST_FMS_ATTITUDE:
                self._axis_id_widget_map[_id].set_axis_value(sp[_id])
        else:
            self._fms_mode_label.set_text ("Disabled")
            for _id in wasp.fms.ID_LIST_FMS_ATTITUDE:
                self._axis_id_widget_map[_id].set_axis_value("")

    def _refresh_label(self):
        try:
            name, sp = self._fms_control.get_mode_and_setpoints()
            self._update_fms_axis_value_labels(True, name, sp)
        except TypeError:
            #no fms enalbed
            self._update_fms_axis_value_labels(False)
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
