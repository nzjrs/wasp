import gtk

import gs.utils as utils

gtk.rc_parse_string("""
    style "plain-progress-bar" {
        engine "murrine" {
            animation = FALSE
            progressbarstyle = 0
        }
    }
    widget "*.PlainProgress" style "plain-progress-bar"
    """)


class ProgressBar(gtk.HBox):
    def __init__(self, range, average=0):
        gtk.HBox.__init__(self, False, 5)
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

        self._lblmin = gtk.Label("%.1f" % self._min)
        self._bar = gtk.ProgressBar()
        self._bar.set_name("PlainProgress")
        self._lblmax = gtk.Label("%.1f" % self._max)

        self.pack_start(self._lblmin, False)
        self.pack_start(self._bar, True)
        self.pack_start(self._lblmax, False)

    def set_value(self, value):
        val = float(value)
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





