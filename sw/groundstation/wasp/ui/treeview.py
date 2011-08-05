import logging
import gobject
import gtk
import time

LOG = logging.getLogger(__name__)

class MessageTreeStore(gtk.TreeStore):

    NAME_IDX,       \
    OBJECT_IDX,     \
    EDITABLE_IDX,   \
    VALUE_IDX,      \
    TIME_IDX =      range(5)

    def __init__(self):
        gtk.TreeStore.__init__(self, 
                str,        #NAME, message.name or field.name
                object,     #OBJECT, message or field underlying python object
                bool,       #EDITABLE, true for fields
                object,     #VALUE, value of field
                int)        #TIME, time last message was received

        self._message_ids = {}

    def add_message(self, message):
        fields = message.get_fields()
        m = self.append(None, ( message.name, message, False, None, int(time.time()) ))
        for f in fields:
            self.append(m, ( f.name, f, True, f.get_default_value(), 0 ))
        return m

    def update_message(self, message, payload, add=True):
        if message.id not in self._message_ids:
            if add:
                self._message_ids[message.id] = self.add_message(message)
            else:
                return

        #get the tree row that represents this message
        _iter = self._message_ids[message.id]
        #and the number of children rows, i.e. fields, of the message
        nkids = self.iter_n_children(_iter)

        vals = message.unpack_values(payload)
        vals = message.get_field_values(vals)
        assert len(vals) == nkids

        #update the time this message was received
        self.set_value(_iter, MessageTreeStore.TIME_IDX, int(time.time()))

        for i in range(nkids):
            self.set_value(
                   self.iter_nth_child(_iter, i),
                   MessageTreeStore.VALUE_IDX,
                   vals[i])

class MessageTreeView(gtk.TreeView):
    def __init__(self, messagetreemodel, editable=True, show_dt=False, show_value=True):
        gtk.TreeView.__init__(self, messagetreemodel)

        self.insert_column_with_attributes(-1, "Name",
                gtk.CellRendererText(),
                text=MessageTreeStore.NAME_IDX)

        if show_value:
            rend = gtk.CellRendererText()
            rend.connect("edited", self._value_edited_cb, messagetreemodel)
            if editable:
                col = gtk.TreeViewColumn("Value", rend, editable=MessageTreeStore.EDITABLE_IDX)
            else:
                col = gtk.TreeViewColumn("Value", rend)
            col.props.expand = True
            col.set_cell_data_func(rend, self._get_field_value)
            self.append_column(col)

        if show_dt:
            self.insert_column_with_data_func(-1, "dt",
                gtk.CellRendererText(),
                self._get_dt_value)

            #schedule a redraw of the time column every second
            gobject.timeout_add(1000, self._redraw_dt, messagetreemodel)


        self.get_selection().set_mode(gtk.SELECTION_SINGLE)

    def _value_edited_cb(self, cellrenderertext, path, new_text, model):
        _iter = model.get_iter(path)
        field = model.get_value(_iter, MessageTreeStore.OBJECT_IDX)
        old = model.get_value(_iter, MessageTreeStore.VALUE_IDX)

        #user deleted value, reset to default
        if new_text == "":
            value = field.get_default_value()
        else:
            #update value if valid, otherwise keep current value
            value = field.interpret_value_from_user_string(new_text, default=old)

        model.set_value(_iter, MessageTreeStore.VALUE_IDX, value)

    def _redraw_dt(self, model):
        _iter = model.get_iter_root()
        while _iter:
            model.row_changed(
                    model.get_path(_iter),
                    _iter)
            _iter = model.iter_next(_iter)
        return True

    def _get_dt_value(self, column, cell, model, _iter):
        txt = ""

        #make sure we set the value on top level, aka message, rows
        if model.iter_depth(_iter) == 0:
            t1 = model.get_value(_iter, MessageTreeStore.TIME_IDX)
            txt = "%ss" % ( int(time.time()) - t1 )

        cell.set_property("text", txt)

    def _get_field_value(self, column, cell, model, _iter):
        value = model.get_value(_iter, MessageTreeStore.VALUE_IDX)

        txt = ""
        #make sure we dont set the value on top level, aka message, rows
        if model.iter_depth(_iter) == 1:
            field = model.get_value(_iter, MessageTreeStore.OBJECT_IDX)
            if value == None:
                value = field.get_default_value()
            txt = field.get_printable_value(value)
        cell.set_property("text", txt)

    def get_selected_message(self):
        model, _iter = self.get_selection().get_selected()

        #make sure something selected
        if not _iter:
            return None

        #make sure a message, not a field is selected
        if model.iter_depth(_iter) == 1:
            _iter = model.iter_parent(_iter)

        return model.get_value(_iter, MessageTreeStore.OBJECT_IDX)

    def get_all_selected_messages(self):
        selected = []
        model, rows = self.get_selection().get_selected_rows()
        for row in rows:
            #row[0] is the toplevel row
            _iter = model.get_iter(row[0])
            if model.iter_is_valid(_iter):
                selected.append(model.get_value(_iter, MessageTreeStore.OBJECT_IDX))
            else:
                LOG.warning("Invalid selection")
        return selected
    
    def get_selected_field(self):
        model, _iter = self.get_selection().get_selected()

        #make sure something selected
        if not _iter:
            return None

        #make sure a field is selected
        if model.iter_depth(_iter) == 1:
            return model.get_value(_iter, MessageTreeStore.OBJECT_IDX)

        return None

    def get_selected_message_and_values(self):
        model, _iter = self.get_selection().get_selected()

        #make sure something selected
        if not _iter:
            return None, None

        #make sure a message, not a field is selected
        if model.iter_depth(_iter) == 1:
            _iter = model.iter_parent(_iter)

        message = model.get_value(_iter, MessageTreeStore.OBJECT_IDX)
        values = []

        _iter = model.iter_children(_iter)
        while _iter:
            val = model.get_value(_iter, MessageTreeStore.VALUE_IDX)
            f = model.get_value(_iter, MessageTreeStore.OBJECT_IDX)
            if f.is_array:
                values += val
            else:
                values.append(val)
            _iter = model.iter_next(_iter)

        return message, values

class SettingsTreeStore(gtk.TreeStore):

    NAME_IDX,           \
    ID_IDX,             \
    SUPPORTS_GET_IDX,   \
    SUPPORTS_SET_IDX,   \
    DYNAMIC_IDX,        \
    OBJECT_IDX =    range(6)

    def __init__(self):
        gtk.TreeStore.__init__(self,
                str,        #NAME, full setting name
                int,        #ID, setting ID
                bool,       #SUPPORTS_GET,
                bool,       #SUPPORTS_SET,
                bool,       #DYNAMIC, ie, SUPPORTS_GET || SUPPORTS_SET
                object)     #OBJECT, the setting object

        self._settings = {}

    def add_section(self, section):
        return self.append( None, (
                    section.name,
                    -1,
                    False,
                    False,
                    False,
                    None))

    def add_setting(self, setting, section=None):
        if setting not in self._settings:
            self._settings[setting] = self.append( section, (
                    setting.name,
                    setting.id,
                    setting.get == 1,
                    setting.set == 1,
                    setting.dynamic,
                    setting) )

class SettingsTreeView(gtk.TreeView):
    def __init__(self, model, show_only_dynamic=False, show_all_colums=True):
        gtk.TreeView.__init__(self)
        self._show_only_dynamic = show_only_dynamic

        self.insert_column_with_attributes(-1, "Name",
                gtk.CellRendererText(),
                text=SettingsTreeStore.NAME_IDX)

        if show_all_colums:
            for name,id_ in (   ("ID", SettingsTreeStore.ID_IDX),
                                ("GET", SettingsTreeStore.SUPPORTS_GET_IDX),
                                ("SET", SettingsTreeStore.SUPPORTS_SET_IDX)):
                self.insert_column_with_attributes(-1, name,
                        gtk.CellRendererText(),
                        text=id_)

        self._filter = None
        self.set_model(model)

    def _visible_func(self, childmodel, _iter):
        if not self._show_only_dynamic:
            return True

        #only show header rows, or rows that are dynamic (editable)
        depth = childmodel.iter_depth(_iter)
        if depth == 0:
            return True

        return childmodel.get_value(_iter, SettingsTreeStore.DYNAMIC_IDX)

    def set_model(self, childmodel):
        if childmodel:
            self._filter = childmodel.filter_new()
            self._filter.set_visible_func(self._visible_func)
            gtk.TreeView.set_model(self, self._filter)

    def show_only_dynamic(self, show):
        self._show_only_dynamic = show
        if self._filter:
            self._filter.refilter()

    def get_selected_setting(self):
        _filter, _iter = self.get_selection().get_selected()

        #make sure something selected
        if not _iter:
            return None

        #make sure it is not a header row, but iter_depth is a method that
        #only exists on the TreeStore, not the treemodelfilter
        model = _filter.get_model()
        if model.iter_depth(_filter.convert_iter_to_child_iter(_iter)) == 0:
            return None

        return _filter.get_value(_iter, SettingsTreeStore.OBJECT_IDX)

