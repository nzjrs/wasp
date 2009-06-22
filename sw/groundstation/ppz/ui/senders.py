import gtk

class _MessageSender(gtk.HBox):
    def __init__(self, messagefile=None):
        gtk.HBox.__init__(self, spacing=4)

        self._messages = {}
        self._model = gtk.ListStore(str, int)

        cb = gtk.ComboBox(self._model)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)
        self.pack_start(cb, expand=True, fill=True)

        btn = gtk.Button("Send")
        btn.connect("clicked", self._on_btn_clicked, cb)
        self.pack_start(btn, expand=False, fill=False)

        if messagefile:
            self.add_message_file(messagefile)

    def _on_btn_clicked(self, btn, cb):
        _iter = cb.get_active_iter()
        if _iter:
            name = self._model.get_value(_iter, 0)
            self.request_send_message(name)

    def add_message_file(self, messagefile):
        raise NotImplementedError

    def request_send_message(self, msg):
        raise NotImplementedError

class SimpleMessageSender(_MessageSender):

    def add_message_file(self, messagefile):
        if messagefile:
            for message in messagefile.get_messages():
                if message and message.id not in self._messages:
                            if len(message.fields) == 0:
                                self._model.append( (message.name, message.id) )
                                self._messages[message.id] = message

    def request_send_message(self, msg):
        print msg

class RequestMessageSender(_MessageSender):

    def add_message_file(self, messagefile):
        if messagefile:
            for message in messagefile.get_messages():
                if message and message.id not in self._messages:
                            if len(message.fields) == 0:
                                self._model.append( (message.name, message.id) )
                                self._messages[message.id] = message

    def request_send_message(self, msg):
        print msg

if __name__ == "__main__":
    w = gtk.Window()
    rm = RequestMessageSender()
    sm = SimpleMessageSender()

    vb = gtk.VBox()
    vb.pack_start(rm)
    vb.pack_start(sm)

    w.add(vb)
    w.show_all()

    gtk.main()
