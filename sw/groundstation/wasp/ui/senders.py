import gobject
import gtk

MESSAGE_NAME_REQUEST_TELEMETRY  = "REQUEST_TELEMETRY"
MESSAGE_NAME_REQUEST_MESSAGE    = "REQUEST_MESSAGE"

class _Sender(gtk.HBox):

    __gsignals__ = {
        "send-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT,          #message
            gobject.TYPE_PYOBJECT]),        #values (tuple)
    }

    def __init__(self):
        gtk.HBox.__init__(self)

    def add_message_file(self, messagefile):
        pass

    def request_send_message(self, msg):
        pass

class _SenderModel(_Sender):
    def __init__(self, *args, **kwargs):
        _Sender.__init__(self, *args, **kwargs)
        self._model = gtk.ListStore(str, object)
        self._model.set_sort_column_id(0, gtk.SORT_ASCENDING)

class _SenderModelComboMixin:
    def __init__(self):
        self._cb = gtk.ComboBox(self._model)
        cell = gtk.CellRendererText()
        self._cb.pack_start(cell, True)
        self._cb.add_attribute(cell, 'text', 0)
        self.pack_start(self._cb, expand=True, fill=True)

        #Change stock icon label
        #http://faq.pygtk.org/index.py?req=show&file=faq09.005.htp
        self._btn = gtk.Button( stock=gtk.STOCK_EXECUTE )
        self._btn.get_children()[0].get_children()[0].get_children()[1].set_text( self.BUTTON_TEXT )
        self._btn.connect("clicked", self._on_btn_clicked)
        self.pack_start(self._btn, expand=False, fill=False)

class _MessageSenderModel(_SenderModel,_SenderModelComboMixin):
    def __init__(self, messagefile=None):
        _SenderModel.__init__(self)
        _SenderModelComboMixin.__init__(self)

        self.set_spacing(4)
        if messagefile:
            self.add_message_file(messagefile)

    def _on_btn_clicked(self, btn):
        _iter = self._cb.get_active_iter()
        if _iter:
            msg = self._model.get_value(_iter, 1)
            self.request_send_message(msg)

class MessageSendButton(_Sender):
    def __init__(self, messagefile, messagename, button=None):
        _Sender.__init__(self)
        self.msg = messagefile.get_message_by_name(messagename)
        if not button:
            button = gtk.Button(self.msg.pretty_name)
        button.connect("clicked", self._on_btn_clicked)
        self.pack_start(button)

    def _on_btn_clicked(self, btn):
        self.emit("send-message", self.msg, ())

class SimpleMessageSender(_MessageSenderModel):

    BUTTON_TEXT = "Send"

    def add_message_file(self, messagefile):
        if messagefile:
            for message in messagefile.get_messages():
                if len(message.fields) == 0:
                    self._model.append( (message.name, message) )

    def request_send_message(self, msg):
        self.emit("send-message", msg, ())

class RequestMessageSender(_MessageSenderModel):

    BUTTON_TEXT = "Request Message"

    def add_message_file(self, messagefile):
        self._rm = None
        if messagefile:
            self._rm = messagefile.get_message_by_name( MESSAGE_NAME_REQUEST_MESSAGE )
            for message in messagefile.get_messages():
                if message.name != MESSAGE_NAME_REQUEST_MESSAGE:
                    self._model.append( (message.name, message) )
        self._cb.set_active(0)

    def request_send_message(self, msg):
        self.emit("send-message", self._rm, (msg.id, ))

class RequestMessageButton(MessageSendButton):
    def __init__(self, messagefile, messagename, button=None):
        self.msgid = messagefile[messagename].id
        if not button:
            button = gtk.Button("Request %s" % messagefile[messagename].pretty_name)
        MessageSendButton.__init__(self, messagefile, MESSAGE_NAME_REQUEST_MESSAGE, button)

    def _on_btn_clicked(self, btn):
        self.emit("send-message", self.msg, (self.msgid,))

class RequestTelemetrySender(RequestMessageSender):

    BUTTON_TEXT = "Request Telemetry"

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

    def add_message_file(self, messagefile):
        RequestMessageSender.add_message_file(self, messagefile)
        if messagefile:
            self._rt = messagefile.get_message_by_name( MESSAGE_NAME_REQUEST_TELEMETRY )

    def request_send_message(self, msg):
        self.emit("send-message", self._rt, (msg.id, float(self._sb.get_value())))

if __name__ == "__main__":
    from wasp.test.testcommon import get_mf, MESSAGE_NAME

    mf = get_mf()

    w = gtk.Window()
    vb = gtk.VBox()

    vb.pack_start(RequestMessageSender(messagefile=mf))
    vb.pack_start(SimpleMessageSender(messagefile=mf))
    vb.pack_start(RequestTelemetrySender(messagefile=mf))
    vb.pack_start(MessageSendButton(messagefile=mf,messagename=MESSAGE_NAME))
    vb.pack_start(RequestMessageButton(messagefile=mf,messagename=MESSAGE_NAME))

    w.add(vb)
    w.show_all()

    gtk.main()
