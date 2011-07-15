import gtk

import gs.utils as utils

#gtk.rc_parse_string("""
#    style "plain-progress-bar" {
#        engine "murrine" {
#            animation = FALSE
#            progressbarstyle = 0
#        }
#    }
#    widget "*.PlainProgress" style "plain-progress-bar"
#    """)

class ProgressBar(gtk.HBox):
    def __init__(self, range, average=0, show_range=True, show_value=True, label="", **kwargs):
        gtk.HBox.__init__(self, False, spacing=5)
        try:
            self._min, self._max = range
            self._auto = False
        except:
            self._auto = True
            self._min = 0.0
            self._max = 0.0
        if average:
            self._avg = utils.MovingAverage(average)
        else:
            self._avg = None

        self._bar = gtk.ProgressBar()
        self._bar.set_name("PlainProgress")

        if show_range:
            self._lblmin = gtk.Label("%.1f" % self._min)
            self._lblmin.props.xalign = 0
            self._lblmax = gtk.Label("%.1f" % self._max)
            self._lblmax.props.xalign = 0

        if label:
            l = gtk.Label(label)
            l.props.xalign = 0
            self.pack_start(l, False, False)

        if show_range:
            self.pack_start(self._lblmin, False)
        self.pack_start(self._bar, True)
        if show_range:
            self.pack_start(self._lblmax, False)

        self._warning_txt = None

    def set_warning_text(self, txt):
        self._warning_txt = txt
        if self._warning_txt:
            self._bar.set_text(self._warning_txt)

    def set_value(self, value):
        val = float(value)
        if not self._warning_txt:
            self._bar.set_text("%.1f" % val)

        if self._avg:
            self._avg.add(val)
            val = self._avg.average()

        if self._auto:
            if val < self._min:
                self._min = val
                self._lblmin.set_text("%.1f" % self._min)
            if val > self._max:
                self._max = val
                self._lblmax.set_text("%.1f" % self._max)

        try:
            frac = ((val - self._min) / (self._max - self._min))
        except ZeroDivisionError:
            frac = 0.0

        if frac < 0:
            frac = 0
        if frac > 1.0:
            frac = 1.0
        self._bar.set_fraction(frac)

    def set_same_size(self, sizegroup):
        sizegroup.add_widget(self._lblmin)
        sizegroup.add_widget(self._lblmax)

if __name__ == "__main__":
    import random
    import gobject

    def newval(_pb):
        _pb.set_value(random.random() * 10.0)
        return True

    p1 = ProgressBar(None)

    w1 = gtk.Window()
    w1.add(p1)
    w1.show_all()
    w1.connect("delete-event", gtk.main_quit)

    gobject.timeout_add(100, newval, p1)

    gtk.main()





