import gtk

class DialogWindow(gtk.Window):
    def __init__(self, name, hide=True, parent=None):
        gtk.Window.__init__(self)
        self.set_title(name)

        if parent:
            self.set_transient_for(parent)
            self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        alignment = gtk.Alignment()
        alignment.set_padding(5,5,5,5)
        self.add(alignment)

        self.vbox = gtk.VBox(spacing=4)
        alignment.add(self.vbox)

        bb = gtk.HButtonBox()
        bb.props.layout_style = gtk.BUTTONBOX_END
        
        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        bb.pack_start(close)

        self.vbox.pack_end(bb)

        self._hide = hide
        if hide:
            self.connect("delete-event", gtk.Widget.hide_on_delete)
        close.connect("clicked", self._clicked)

    def _clicked(self, *args):
        if self._hide:
            self.hide()
        else:
            self.destroy()

if __name__ == "__main__":
    w = DialogWindow("test", False)
    w.vbox.pack_start(gtk.Label("test"))
    w.show_all()
    gtk.main()
