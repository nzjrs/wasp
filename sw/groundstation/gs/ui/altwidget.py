import gtk
import pango

import gs
import gs.ui.custom as custom

class AltWidget(custom.GdkWidget):

    DEFAULT_HEIGHT = 60
    VISIBLE_STEPS = 5
    ALT_STEPS = 20
    ALT_RANGE = 100

    def __init__(self):
        custom.GdkWidget.__init__(self)
        self.set_size_request(-1, self.DEFAULT_HEIGHT)

        #altitude in M
        self.min_alt = -10.
        self.max_alt = 90.
        self.alt = 0.
        self.alt_pixel_x = None

    def setup_gcs(self, drawable):
        self.linegc = drawable.new_gc()
        self.linegc.set_line_attributes(1, gtk.gdk.LINE_SOLID,
                                    gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)

        self.redgc = drawable.new_gc(
                        foreground=self.get_color(drawable, r=1.0, g=0.0, b=0.0),
                        fill=gtk.gdk.SOLID,
                        line_width=1)

        self.pc = self.get_pango_context()

    def do_draw(self, drawable):
        steps = gs.linspace(0, self.height, self.VISIBLE_STEPS)
        stepvals = gs.linspace(self.min_alt, self.max_alt, self.VISIBLE_STEPS)

        stepvals.reverse()
        for i in range(len(steps)):
            y = int(steps[i])
            val = stepvals[i]

            #do not draw top or bottom lines
            if y != 0 and y != self.height:
                drawable.draw_line(self.linegc,0, y, self.width, y)

            #draw the label, skipping the top one
            if y != 0:
                layout = pango.Layout(self.pc)
                layout.set_text("%.0f m" % val)
                w,h = layout.get_pixel_size()
                drawable.draw_layout(self.linegc, 1,y-h, layout)

        #draw the altitude marker
        if self.alt_pixel_x != None:
            alt = (self.alt - self.min_alt) / (self.max_alt - self.min_alt)
            alt_pixel_y = self.height - int(alt * self.height)

            w = 10
            drawable.draw_arc(self.redgc, True, self.alt_pixel_x-w/2, alt_pixel_y-w/2, w, w, 0, 360*64)
            drawable.draw_line(self.redgc, self.alt_pixel_x, alt_pixel_y, self.alt_pixel_x, self.height)

            #debug
            if False:
                print "ALT: %.1f <= %.1f <= %.1f" % (self.min_alt, self.alt, self.max_alt)
                print "DRAW: alt %f = %dpx (h=%d, top@0)" % (self.alt, alt_pixel_y, self.height)

                drawable.draw_line(self.redgc, 0, alt_pixel_y, self.width, alt_pixel_y)

                layout = pango.Layout(self.pc)
                layout.set_text("%2.1f" % self.alt)
                w,h = layout.get_pixel_size()
                drawable.draw_layout(self.redgc, 32, 10, layout)

    def update_altitude(self, alt):

        alt = float(alt)

        #adjust range in steps while snapping to 10
        step = self.ALT_STEPS
        total_range = self.ALT_RANGE
        if alt < self.min_alt:
            self.min_alt = alt - step - (alt % 10)
            self.max_alt = self.min_alt + total_range
        if alt > self.max_alt:
            self.max_alt = alt + step - (alt % 10)
            self.min_alt = self.max_alt - total_range

        self.alt = alt
        self.queue_draw()

    def update_pixel_x(self, x):
        self.alt_pixel_x = x
        self.queue_draw()

    def update_pixel_x_and_altitude(self, x, alt):
        self.alt_pixel_x = x
        self.update_altitude(alt)
