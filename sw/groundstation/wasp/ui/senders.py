import gobject
import gtk

class _MessageSender(gtk.HBox):

    __gsignals__ = {
        "send-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT,      #message
            gobject.TYPE_PYOBJECT]),     #values (tuple)
    }

    def __init__(self, messagefile=None):
        gtk.HBox.__init__(self, spacing=4)

        self._model = gtk.ListStore(str, object)

        self._cb = gtk.ComboBox(self._model)
        cell = gtk.CellRendererText()
        self._cb.pack_start(cell, True)
        self._cb.add_attribute(cell, 'text', 0)
        self.pack_start(self._cb, expand=True, fill=True)

        self._btn = gtk.Button( stock=gtk.STOCK_EXECUTE )
        #Change stock icon label
        #http://faq.pygtk.org/index.py?req=show&file=faq09.005.htp
        self._btn.get_children()[0].get_children()[0].get_children()[1].set_text( self.BUTTON_TEXT )
        self._btn.connect("clicked", self._on_btn_clicked)
        self.pack_start(self._btn, expand=False, fill=False)

        if messagefile:
            self.add_message_file(messagefile)

    def _on_btn_clicked(self, btn):
        _iter = self._cb.get_active_iter()
        if _iter:
            msg = self._model.get_value(_iter, 1)
            self.request_send_message(msg)

    def add_message_file(self, messagefile):
        raise NotImplementedError

    def request_send_message(self, msg):
        raise NotImplementedError

class SimpleMessageSender(_MessageSender):

    BUTTON_TEXT = "Send"

    def add_message_file(self, messagefile):
        if messagefile:
            for message in messagefile.get_messages():
                if len(message.fields) == 0:
                    self._model.append( (message.name, message) )

    def request_send_message(self, msg):
        self.emit("send-message", msg, ())

class RequestMessageSender(_MessageSender):

    BUTTON_TEXT = "Request Message"
    REQUEST_MESSAGE_NAME = "REQUEST_MESSAGE"

    def add_message_file(self, messagefile):
        self._rm = None
        if messagefile:
            self._rm = messagefile.get_message_by_name( self.REQUEST_MESSAGE_NAME )
            for message in messagefile.get_messages():
                if message.name != self.REQUEST_MESSAGE_NAME:
                    self._model.append( (message.name, message) )

    def request_send_message(self, msg):
        self.emit("send-message", self._rm, (msg.id, ))

class RequestTelemetrySender(RequestMessageSender):

    BUTTON_TEXT = "Request Telemetry"
    REQUEST_MESSAGE_NAME = "REQUEST_TELEMETRY"

    def __init__(self, *args, **kwargs):
        RequestMessageSender.__init__(self, *args, **kwargs)
        
        hb = gtk.HBox()
        hb.pack_start(gtk.Label("Frequency: "), expand=False)
        
        self._sb = gtk.SpinButton(digits=1)
        self._sb.set_increments(0.5, 1)
        self._sb.set_range(0.0, 60)
        hb.pack_start(self._sb, expand=False)
        
        self.pack_start(hb, expand=False, fill=True)
        self.reorder_child(hb, 1)

    def request_send_message(self, msg):
        self.emit("send-message", self._rm, (msg.id, self._sb.get_value()))

class _SettingsSender(gtk.HBox):

    __gsignals__ = {
        "send-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT,      #message
            gobject.TYPE_PYOBJECT]),    #values (tuple)
    }

    def __init__(self, settingsfile):
        gtk.HBox.__init__(self, spacing=4)

        self._model = gtk.ListStore(str, object)

        self._cb = gtk.ComboBox(self._model)
        cell = gtk.CellRendererText()
        self._cb.pack_start(cell, True)
        self._cb.add_attribute(cell, 'text', 0)
        self.pack_start(self._cb, expand=True, fill=True)

        self._btn = gtk.Button( stock=gtk.STOCK_EXECUTE )
        #Change stock icon label
        #http://faq.pygtk.org/index.py?req=show&file=faq09.005.htp
        self._btn.get_children()[0].get_children()[0].get_children()[1].set_text( self.BUTTON_TEXT )
        self._btn.connect("clicked", self._on_btn_clicked)
        self.pack_start(self._btn, expand=False, fill=False)

        if messagefile:
            self.add_message_file(messagefile)

    def _on_btn_clicked(self, btn):
        _iter = self._cb.get_active_iter()
        if _iter:
            msg = self._model.get_value(_iter, 1)
            self.request_send_message(msg)

    def add_message_file(self, messagefile):
        raise NotImplementedError

    def request_send_message(self, msg):
        raise NotImplementedError


if __name__ == "__main__":
    w = gtk.Window()
    rm = RequestMessageSender()
    sm = SimpleMessageSender()
    tm = RequestTelemetrySender()

    vb = gtk.VBox()
    vb.pack_start(rm)
    vb.pack_start(sm)
    vb.pack_start(tm)

    w.add(vb)
    w.show_all()

    gtk.main()
