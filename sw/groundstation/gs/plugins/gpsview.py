import gtk
import math
import os.path
import logging
import subprocess

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('gpsview')

class GpsView(plugin.Plugin):
    def __init__(self, conf, source, messages_file, groundstation_window):

        pb = gs.ui.get_icon_pixbuf("world.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Show Detailed GPS Info")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("Window", item)

        source.register_interest(self._on_gps_gsv, 0, "GPS_GSV")

        self._sky = None
        self._w = None
        self._sats = {}

    def _on_gps_gsv(self, msg, header, payload):
        if self._sky:
            sv,prn,elevation,azimuth,snr = msg.unpack_values(payload)
            self._sats[prn] = Sat(prn,elevation,azimuth,snr)
            #Maybe should cap the redraw rate here...
            self._sky.redraw(self._sats.values())

    def _create_window(self):
        self._w = gtk.Window()
        self._w.connect("delete-event", gtk.Widget.hide_on_delete)
        self._sky = SkyView()
        self._w.add(self._sky)

    def _show_window(self, *args):
        if not self._w:
            self._create_window()
        self._w.show_all()

# Fake the libgps API, make this Sat class have the same elements as expected
# by the skyview
class Sat:
    def __init__(self,prn,elevation,azimuth,snr):
        self.PRN = prn
        self.azimuth = azimuth
        self.elevation = elevation
        self.ss = snr
        self.used = True

# Taken from xgps (of the gpsd project)
# http://git.berlios.de/cgi-bin/cgit.cgi/gpsd/tree/xgps
class SkyView(gtk.DrawingArea):
    "Satellite skyview, encapsulates pygtk's draw-on-expose behavior."
    # See <http://faq.pygtk.org/index.py?req=show&file=faq18.008.htp>
    HORIZON_PAD = 20	# How much whitespace to leave around horizon
    SAT_RADIUS = 5	# Diameter of satellite circle
    GPS_PRNMAX = 32	# above this number are SBAS satellites
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(400, 400)
        self.gc = None  # initialized in realize-event handler
        self.width  = 0 # updated in size-allocate handler
        self.height = 0 # updated in size-allocate handler
        self.connect('size-allocate', self.on_size_allocate)
        self.connect('expose-event',  self.on_expose_event)
        self.connect('realize',       self.on_realize)
        self.pangolayout = self.create_pango_layout("")
        self.satellites = []

    def on_realize(self, widget):
        self.gc = widget.window.new_gc()
        self.gc.set_line_attributes(1, gtk.gdk.LINE_SOLID,
                                    gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)

    def on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        self.diameter = min(self.width, self.height) - SkyView.HORIZON_PAD

    def set_color(self, spec):
        "Set foreground color for draweing."
        self.gc.set_rgb_fg_color(gtk.gdk.color_parse(spec))

    def draw_circle(self, widget, x, y, diam, filled=False):
        "Draw a circle centered on the specified midpoint."
        widget.window.draw_arc(self.gc, filled,
                               x - diam / 2, y - diam / 2,
                               diam, diam, 0, 360 * 64)

    def draw_square(self, widget, x, y, diam, filled=False):
        "Draw a square centered on the specified midpoint."
        widget.window.draw_rectangle(self.gc, filled,
                                     x - diam / 2, y - diam / 2,
                                     diam, diam)

    def draw_string(self, widget, x, y, letter):
        "Draw a letter on the skyview."
        self.pangolayout.set_text(letter)
        # FIXME: When the layout object can report its size, use it
        self.window.draw_layout(self.gc, x-5, y-10, self.pangolayout)

    def pol2cart(self, az, el):
        "Polar to Cartesian coordinates within the horizon circle."
        az *= (math.pi/180)	# Degrees to radians
        # Exact spherical projection would be like this:
        # el = sin((90.0 - el) * DEG_2_RAD);
        el = ((90.0 - el) / 90.0);
        xout = int((self.width / 2) + math.sin(az) * el * (self.diameter / 2))
        yout = int((self.height / 2) - math.cos(az) * el * (self.diameter / 2))
        return (xout, yout)

    def on_expose_event(self, widget, event):
        self.set_color("white")
        widget.window.draw_rectangle(self.gc, True, 0,0, self.width,self.height)
        # The zenith marker
        self.set_color("gray")
        self.draw_circle(widget, self.width / 2, self.height / 2, 6)
        # The circle corresponding to 45 degrees elevation.
        # There are two ways we could plot this.  Projecting the sphere
        # on the display plane, the circle would have a diameter of
        # sin(45) ~ 0.7.  But the naive linear mapping, just splitting
        # the horizon diameter in half, seems to work better visually.
        self.draw_circle(widget, self.width / 2, self.height / 2,
                         int(self.diameter * 0.5))
        self.set_color("black")
        # The horizon circle
        self.draw_circle(widget, self.width / 2, self.height / 2,
                         self.diameter)
        # The compass-point letters
        (x, y) = self.pol2cart(0, 0)
        self.draw_string(widget, x, y+10, "N")
        (x, y) = self.pol2cart(90, 0)
        self.draw_string(widget, x-10, y, "E")
        (x, y) = self.pol2cart(180, 0)
        self.draw_string(widget, x, y-10, "S")
        (x, y) = self.pol2cart(270, 0)
        self.draw_string(widget, x+10, y, "W")
        # The satellites
        for sat in self.satellites:
            (x, y) = self.pol2cart(sat.azimuth, sat.elevation)
            if sat.ss < 10:
                self.set_color("Black")
            elif sat.ss < 30:
                self.set_color("Red")
            elif sat.ss < 35:
                self.set_color("Yellow");
            elif sat.ss < 40:
                self.set_color("Green3");
            else:
                self.set_color("Green1");
            if sat.PRN > SkyView.GPS_PRNMAX:
                self.draw_square(widget,
                                 x-SkyView.SAT_RADIUS, y-SkyView.SAT_RADIUS,
                                 2 * SkyView.SAT_RADIUS + 1, sat.used);
            else:
                self.draw_circle(widget,
                                 x-SkyView.SAT_RADIUS, y-SkyView.SAT_RADIUS,
                                 2 * SkyView.SAT_RADIUS + 1, sat.used);
            self.set_color("Black")
            self.draw_string(widget, x, y+10, str(sat.PRN))
    def redraw(self, satellites):
        "Redraw the skyview."
        self.satellites = satellites
        self.queue_draw()
