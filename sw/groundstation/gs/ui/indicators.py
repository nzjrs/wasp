import gobject
import gtk

import gs.ui

class _Colorable:

    BLANK       = None
    GREEN       = 0x33FF00FF
    YELLOW      = 0xFFFF00FF
    RED         = 0xFF0000FF

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

class ColorBox(gtk.Image, _Colorable):

    #share these between instances for efficiency
    GREEN_PB = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    GREEN_PB.fill(pixel=_Colorable.GREEN)
    YELLOW_PB = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    YELLOW_PB.fill(pixel=_Colorable.YELLOW)
    RED_PB = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width=16, height=16)
    RED_PB.fill(pixel=_Colorable.RED)

    def __init__(self):
        gtk.Image.__init__(self)
        _Colorable.__init__(self)

    def set_color(self, color):
        if color == self.GREEN:
            self.set_from_pixbuf(self.GREEN_PB)
        elif color == self.YELLOW:
            self.set_from_pixbuf(self.YELLOW_PB)
        elif color == self.RED:
            self.set_from_pixbuf(self.RED_PB)
        else:
            self.clear()


class FadingColorBox(ColorBox):

    FPS = 10

    def __init__(self, fade_time=2):
        ColorBox.__init__(self)
        self._fade_time = fade_time

        tick = 1000/self.FPS
        self._timout = gobject.timeout_add(tick, self._animate)
        self._animating = False

        #caclulate the fade increment
        self._opacity = 0.0
        self._fade_increment = 255.0 / ((fade_time * 1000.0) / tick)

        self._pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, width=16, height=16)
        self.set_from_pixbuf(self._pb)

    def _update(self, opacity):
        self._pb.fill(pixel=self._color - int(opacity))
        self.set_from_pixbuf(self._pb)

    def set_color(self, color):
        self._color = color
        self._opacity = 0.0
        self._animating = True
        self._update(self._opacity)

    def _animate(self):
        if self._animating:
            self._opacity += self._fade_increment
            if self._opacity > 255.0:
                self._opacity = 255.0
                self._animating = False

            self._update(self._opacity)
        return True


class ColorLabelBox(gtk.HBox, _Colorable):

    def __init__(self, text="", right=False):
        gtk.HBox.__init__(self)
        _Colorable.__init__(self)

        if text and not right:
            self.pack_start(gs.ui.make_label(text, 0), False, True)

        self._box = ColorBox()
        self._box.set_red()
        self.pack_start(self._box)

        if text and right:
            self.pack_start(gs.ui.make_label(text, 0), False, True)

    def set_red(self):
        self._box.set_red()

    def set_yellow(self):
        self._box.set_yellow()

    def set_green(self):
        self._box.set_green()

    def set_color(self, color):
        self._box.set_color(color)

class ColorLabel(gtk.EventBox, _Colorable):

    #share these between instances for efficiency
    GREEN_COLOR = gtk.gdk.Color(
                (_Colorable.GREEN & 0xFF000000) >> 16,
                (_Colorable.GREEN & 0x00FF0000) >> 8,
                _Colorable.GREEN & 0x0000FF00, 0)
    YELLOW_COLOR = gtk.gdk.Color(
                (_Colorable.YELLOW & 0xFF000000) >> 16,
                (_Colorable.YELLOW & 0x00FF0000) >> 8,
                _Colorable.YELLOW & 0x0000FF00, 0)
    RED_COLOR = gtk.gdk.Color(
                (_Colorable.RED & 0xFF000000) >> 16,
                (_Colorable.RED & 0x00FF0000) >> 8,
                _Colorable.RED & 0x0000FF00, 0)

    def __init__(self, text):
        gtk.EventBox.__init__(self)
        _Colorable.__init__(self)

        label = gtk.Label(text)
        self.add(label)

    def set_color(self, color):
        if color == self.GREEN:
            self.modify_bg(gtk.STATE_NORMAL, self.GREEN_COLOR)
        elif color == self.YELLOW:
            self.modify_bg(gtk.STATE_NORMAL, self.YELLOW_COLOR)
        elif color == self.RED:
            self.modify_bg(gtk.STATE_NORMAL, self.RED_COLOR)
        else:
            #FIXME: Not supported...
            pass



if __name__ == "__main__":
    import random

    w = gtk.Window()
    w.set_default_size(150,50)

    vb = gtk.VBox()

    box = ColorLabelBox("box")
    box.set_red()

    lbl = ColorLabel("test")
    lbl.set_yellow()

    fade = FadingColorBox()
    fade.set_green()

    def change(btn, box, lbl):
        box.set_green()
        lbl.set_green()

    btn = gtk.Button("Change")
    btn.connect("clicked", change, box, lbl)

    def randomchange(btn, box):
        funcs = (box.set_red, box.set_yellow, box.set_green)
        funcs[random.randint(0,2)]()

    btn2 = gtk.Button("Random Fade")
    btn2.connect("clicked", randomchange, fade)

    vb.pack_start(lbl, False, False)
    vb.pack_start(box, False, False)
    vb.pack_start(btn, False, False)
    vb.pack_start(fade, False, False)
    vb.pack_start(btn2, False, False)



    w.add(vb)
    w.show_all()
    gtk.main()


        

