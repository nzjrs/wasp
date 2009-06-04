#!/usr/bin/env python
#
# A simple example of using multiple HScrollLineGraph widgets
#
# -- Micah Dowty <micah@picogui.org>
#

import gtk
import time, math, re
import gs.ui.rtgraph as rtgraph

windows = []

class SineChannel(rtgraph.Channel):
    def __init__(self, frequency, amplitude, color):
        rtgraph.Channel.__init__(self, color=color)
        self.frequency = frequency
        self.amplitude = amplitude

    def getValue(self):
        return math.sin((time.time() * self.frequency) % (math.pi*2)) * 0.5 * self.amplitude + 0.5

class CPUActivityChannel(rtgraph.Channel):
    lastStatValues = None
    activity = None

    def readCpuStat(self):
        """Reads the 'cpu' line in /proc/stat"""
        f = open("/proc/stat")
        for line in f.xreadlines():
            if line.startswith("cpu "):
                cpu, user, nice, sys, idle = re.split("\s+", line.strip())[:5]
                break
        f.close()
        return (long(user) + long(nice + sys), long(idle))

    def getValue(self):
        newStatValues = self.readCpuStat()

        if self.lastStatValues:
            active = newStatValues[0] - self.lastStatValues[0]
            idle = newStatValues[1] - self.lastStatValues[1]
            if active + idle > 0:
                self.activity = active / (active + idle)

        self.lastStatValues = newStatValues
        return self.activity

class UI:
    def __init__(self):
        self._windows = [
            self._make_cpu_graph(),
            self._make_scroll_graph(),
            self._make_tweak_graph()
        ]

    def _make_cpu_graph(self):
        g = rtgraph.HScrollAreaGraph(
            scrollRate = 4,
            pollInterval = 200,
            size       = (128,48),
            gridSize   = 8,
            channels   = [CPUActivityChannel(color=(1, 1, 1))],
            bgColor    = (0, 0, 0.3),
            gridColor  = (0, 0, 0.5),
            )
        g.show()

        w = gtk.Window()
        w.set_title("CPU Load")
        w.add(g)
        w.show()
        w.connect("destroy", self._quit)
        return w

    def _make_scroll_graph(self):
        w = gtk.Window()
        vbox = gtk.VBox()
        vbox.show()
        w.add(vbox)
        w.set_border_width(5)

        for name, rate, channels in [
            ("Sub-ether phase", 80, [SineChannel(2, 0.8, (0,0,1)),
                                     rtgraph.Channel(0.5, (0,0,0))]),
            ("Tachyon variance", 30, [SineChannel(1, 1, (0,0,1)),
                                      SineChannel(1.01, 1, (0,0.5,0)),
                                      SineChannel(10, 0.4, (1,0,0))]),
            ]:

            graph = rtgraph.HScrollLineGraph(scrollRate=rate)
            graph.channels = channels
            graph.show()

            frame = gtk.Frame()
            frame.set_label(name)
            frame.add(graph)
            frame.show()

            vbox.pack_end(frame)

        w.show()
        w.connect("destroy", self._quit)
        return w

    def _make_tweak_graph(self):
        w = gtk.Window()
        vbox = gtk.VBox()
        vbox.show()
        w.add(vbox)
        w.set_border_width(5)

        graph = rtgraph.HScrollLineGraph(channels=[
            rtgraph.Channel(0, color=(1,0,0)),
            rtgraph.Channel(0, color=(0,0.8,0)),
            rtgraph.Channel(0, color=(0,0,1)),
            ])
        graph.show()
        frame = gtk.Frame()
        frame.add(graph)
        frame.show()
        vbox.pack_start(frame)

        tweaker = rtgraph.Tweak.List([
            rtgraph.Tweak.Quantity(graph.channels[0], 'value', name="Red"),
            rtgraph.Tweak.Quantity(graph.channels[1], 'value', name="Green"),
            rtgraph.Tweak.Quantity(graph.channels[2], 'value', name="Blue"),
            ])
        tweaker.show()
        vbox.pack_start(tweaker, False)

        w.show()
        w.connect("destroy", self._quit)
        return w


    def _quit(self, w):
        self._windows.remove(w)
        if not self._windows:
            gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    u = UI()
    u.main()

