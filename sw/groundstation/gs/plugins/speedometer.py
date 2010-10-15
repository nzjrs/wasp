import gtk
import cairo
import os.path
import logging
import random
from math import pi
from math import cos
from math import sin

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('speedometer')

class Speedometer(plugin.Plugin):
    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):

        pb = gs.ui.get_icon_pixbuf("world.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Show GPS Speed")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._show_window)
        groundstation_window.add_submenu_item("Window", "GPS", item)

        source.register_interest(self._on_gps_vtg, 0, "GPS_VTG")

        self._speedo = None
        self._w = None

    def _on_gps_vtg(self, msg, header, payload):
        if self._speedo:
            track,speed = msg.unpack_values(payload)
            self._speedo.update_speed(speed)

    def _create_window(self):
        self._w = gtk.Window()
        self._w.connect("delete-event", gtk.Widget.hide_on_delete)
        self._speedo = Speedometer("kmh")
        self._w.add(self._speedo)

    def _show_window(self, *args):
        if not self._w:
            self._create_window()
        self._w.show_all()

# Taken from xgpsspeed (of the gpsd project)
# http://git.berlios.de/cgi-bin/cgit.cgi/gpsd/tree/xgpsspeed
class Speedometer(gtk.DrawingArea):
    def __init__(self, speed_unit=None):
        gtk.DrawingArea.__init__(self)
        self.connect('expose_event', self.expose_event)
        self.long_ticks = (2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8)
        self.short_ticks = (0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9)
        self.long_inset = lambda x: 0.1 * x
        self.middle_inset = lambda x: self.long_inset(x) / 1.5
        self.short_inset = lambda x: self.long_inset(x) / 3
        self.res_div = 10.0
        self.res_div_mul = 1
        self.last_speed = 0
        self.MPS_TO_KPH = 3.6000000000000001
        self.MPS_TO_MPH = 2.2369363
        self.MPS_TO_KNOTS = 1.9438445
        self.MPH_UNIT_LABEL = 'mph'
        self.KPH_UNIT_LABEL = 'kmh'
        self.KNOTS_UNIT_LABEL = 'knots'
        self.conversions = {
                self.MPH_UNIT_LABEL: self.MPS_TO_MPH,
                self.KPH_UNIT_LABEL: self.MPS_TO_KPH,
                self.KNOTS_UNIT_LABEL: self.MPS_TO_KNOTS
        }
        self.speed_unit = speed_unit or self.MPH_UNIT_LABEL
        if not self.speed_unit in self.conversions:
            raise TypeError(
                    '%s is not a valid speed unit'
                    %(repr(speed_unit))
            )
        self.nums = {
                -8:  0,
                -7: 10,
                -6: 20,
                -5: 30,
                -4: 40,
                -3: 50,
                -2: 60,
                -1: 70,
                0:  80,
                1:  90,
                2: 100
        }


    def expose_event(self, widget, event, data=None):
        self.cr = self.window.cairo_create()
        self.cr.rectangle(
                event.area.x,
                event.area.y,
                event.area.width,
                event.area.height
        )
        self.cr.clip()
        x, y = self.get_x_y()
        width, height = self.window.get_size()
        radius = self.get_radius(width, height)
        self.cr.set_line_width(radius / 100)
        self.draw_arc_and_ticks(width, height, radius, x, y)
        self.draw_needle(self.last_speed, radius, x, y)
        self.draw_speed_text(self.last_speed, radius, x, y)

    def draw_arc_and_ticks(self, width, height, radius, x, y):
        self.cr.set_source_rgb(1.0, 1.0, 1.0)
        self.cr.rectangle(0, 0, width, height)
        self.cr.fill()
        self.cr.set_source_rgb(0.0, 0.0, 0.0)

        #draw the speedometer arc
        self.cr.arc_negative(
                x,
                y,
                radius,
                self.degrees_to_radians(60),
                self.degrees_to_radians(120)
        )
        self.cr.stroke()
        long_inset = self.long_inset(radius)
        middle_inset = self.middle_inset(radius)
        short_inset = self.short_inset(radius)

        #draw the ticks
        for i in self.long_ticks:
            self.cr.move_to(
                    x + (radius - long_inset) * cos(i * pi / 6.0),
                    y + (radius - long_inset) * sin(i * pi / 6.0)
            )
            self.cr.line_to(
                    x + (radius + (self.cr.get_line_width() / 2)) * cos(i * pi
                        / 6.0),
                    y + (radius + (self.cr.get_line_width() / 2)) * sin(i * pi
                        / 6.0)
            )
            self.cr.select_font_face(
                    'Georgia',
                    cairo.FONT_SLANT_NORMAL,
            )
            self.cr.set_font_size(radius / 10)
            self.cr.save()
            _num = str(self.nums.get(i) * self.res_div_mul)
            (
                    x_bearing,
                    y_bearing,
                    t_width,
                    t_height,
                    x_advance,
                    y_advance
            )  =  self.cr.text_extents(_num)

            if i in (-8, -7, -6, -5, -4):
                self.cr.move_to(
                        (x + (radius - long_inset - (t_width / 2)) * cos(i * pi
                            / 6.0)),
                        (y + (radius - long_inset - (t_height * 2)) * sin(i * pi
                            / 6.0))
                )
            elif i in (-2, -1, 0, 2, 1):
                self.cr.move_to(
                        (x + (radius - long_inset - (t_width * 1.5 )) * cos(i * pi
                            / 6.0)),
                        (y + (radius - long_inset - (t_height * 2 )) * sin(i * pi
                            / 6.0))
                )
            elif i in (-3,):
                self.cr.move_to(
                        (x - t_width / 2), (y - radius +
                            self.long_inset(radius) * 2 + t_height)
                )
            self.cr.show_text(_num)
            self.cr.restore()

            if i != self.long_ticks[0]:
                self.cr.move_to(
                        x + (radius - middle_inset) * cos((i + 0.5) * pi / 6.0),
                        y + (radius - middle_inset) * sin((i + 0.5) * pi / 6.0)
                )
                self.cr.line_to(
                        x + (radius + (self.cr.get_line_width() / 2)) * cos((i
                            + 0.5) * pi / 6.0),
                        y + (radius + (self.cr.get_line_width() / 2)) * sin((i
                            + 0.5) * pi / 6.0)
                )

            for z in self.short_ticks:
                if i < 0:
                    self.cr.move_to(
                            x + (radius - short_inset) * cos((i + z) * pi / 6.0),
                            y + (radius - short_inset) * sin((i + z) * pi / 6.0)
                    )
                    self.cr.line_to(
                            x + (radius + (self.cr.get_line_width() / 2)) * cos((i
                                + z) * pi / 6.0),
                            y + (radius + (self.cr.get_line_width() / 2)) * sin((i
                                + z) * pi / 6.0)
                    )
                else:
                    self.cr.move_to(
                            x + (radius - short_inset) * cos((i - z) * pi / 6.0),
                            y + (radius - short_inset) * sin((i - z) * pi / 6.0)
                    )
                    self.cr.line_to(
                            x + (radius + (self.cr.get_line_width() / 2)) * cos((i
                                - z) * pi / 6.0),
                            y + (radius + (self.cr.get_line_width() / 2)) * sin((i
                                - z) * pi / 6.0)
                    )
            self.cr.stroke()

    def draw_needle(self, speed, radius, x, y):
        self.cr.save()
        inset = self.long_inset(radius)
        speed = speed * self.conversions.get(self.speed_unit)
        speed = speed / (self.res_div * self.res_div_mul)
        actual = self.long_ticks[-1] + speed
        if actual > self.long_ticks[0]:
            #TODO test this in real conditions! ;)
            self.res_div_mul += 1
            speed = speed / (self.res_div * self.res_div_mul)
            actual = self.long_ticks[-1] + speed
        self.cr.move_to(x, y)
        self.cr.line_to(
                x + (radius - (2 * inset)) * cos(actual * pi / 6.0),
                y + (radius - (2 * inset)) * sin(actual * pi / 6.0)
        )
        self.cr.stroke()
        self.cr.restore()

    def draw_speed_text(self, speed, radius, x, y):
        self.cr.save()
        speed = '%.2f %s'  %(
                speed * self.conversions.get(self.speed_unit),
                self.speed_unit
        )
        self.cr.select_font_face(
                'Georgia',
                cairo.FONT_SLANT_NORMAL,
                #cairo.FONT_WEIGHT_BOLD
        )
        self.cr.set_font_size(radius / 10)
        x_bearing, y_bearing, t_width, t_height = self.cr.text_extents(speed)[:4]
        self.cr.move_to((x - t_width / 2), (y + radius) - self.long_inset(radius))
        self.cr.show_text(speed)
        self.cr.restore()


    def degrees_to_radians(self, degrees):
        return ((pi / 180) * degrees)

    def radians_to_degrees(self, radians):
        return ((pi * 180) / radians)

    def get_x_y(self):
        rect = self.get_allocation()
        x = (rect.x + rect.width / 2.0)
        y = (rect.y + rect.height / 2.0) - 20
        return x, y

    def get_radius(self, width, height):
        return min(width / 2.0, height / 2.0) - 20

    def update_speed(self, kmh):
        #the internal representation is mph
        self.last_speed = kmh * 0.621371192
        self.queue_draw()


