import gtk

class GdkWidget(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.width  = 0 # updated in size-allocate handler
        self.height = 0 # idem
        self.connect('size-allocate', self._on_size_allocate)
        self.connect('expose-event',  self._on_expose_event)
        self.connect('realize',       self._on_realize)

    def get_color(self, drawable, r, g, b):
        """
        Returns a GdkColor for the drawables colormap with the specified
        reg, green and blue values. 
        
        0.0 <= r,g,b <= 1.0)
        """
        color = (r, g, b)
        return drawable.get_colormap().alloc_color(*[int(c * 65535) for c in color])

    def _on_realize(self, widget):
        self.setup_gcs(widget.window)

    def _on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height

    def _on_expose_event(self, widget, event):
        self.do_draw(widget.window)

    def setup_gcs(self, drawable):
        raise NotImplementedError

    def do_draw(self, drawable):
        raise NotImplementedError

