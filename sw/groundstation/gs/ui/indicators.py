import gtk

import gs.ui

class _Colorable:
    def __init__(self):
        self._color = self.BLANK

    def set_red(self):
        if self._color != self.RED:
            self.set_color(self.RED)
        self._color = self.RED

    def set_yellow(self):
        if self._color != self.YELLOW:
            self.set_color(self.YELLOW)
        self._color = self.YELLOW

    def set_green(self):
        if self._color != self.GREEN:
            self.set_color(self.GREEN)
        self._color = self.GREEN

    def set_color(self):
        raise NotImplementedError

class ColorLabelBox(gtk.HBox, _Colorable):

    BLANK = None
    GREEN = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    GREEN.fill(pixel=int("0x33FF00FF", 0))
    YELLOW = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    YELLOW.fill(pixel=int("0xFFFF00FF", 0))
    RED = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    RED.fill(pixel=int("0xFF0000FF", 0))

    def __init__(self, text="", right=False):
        gtk.HBox.__init__(self)
        _Colorable.__init__(self)

        if text and not right:
            self.pack_start(gs.ui.make_label(text, 0), False, True)

        self._img = gtk.Image()
        self.set_red()
        self.pack_start(self._img)

        if text and right:
            self.pack_start(gs.ui.make_label(text, 0), False, True)

    def set_color(self, color):
        self._img.set_from_pixbuf(color)

class ColorLabel(gtk.EventBox, _Colorable):

    BLANK = None
    GREEN = gtk.gdk.color_parse("#33FF00")
    YELLOW = gtk.gdk.color_parse("#FFFF00")
    RED = gtk.gdk.color_parse("#FF0000")

    def __init__(self, text):
        gtk.EventBox.__init__(self)
        _Colorable.__init__(self)

        label = gtk.Label(text)
        self.add(label)

    def set_color(self, color):
        self.modify_bg(gtk.STATE_NORMAL, color)

if __name__ == "__main__":
    w = gtk.Window()

    lbl = ColorLabel("test")
    lbl.set_yellow()

    w.add(lbl)
    w.show_all()
    gtk.main()


        

