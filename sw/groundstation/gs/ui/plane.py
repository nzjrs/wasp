import math
import os.path
import gtk.gtkgl

from OpenGL.GL import *
from OpenGL.GLU import *

class PlaneView(gtk.Window):
    def __init__(self, source):
        gtk.Window.__init__(self)

        self.set_default_size(500, 400)
        self.set_title("Plane View")
        self.connect("delete-event", self._on_window_delete)

        self.plane = _PlaneWidget(source) 
        self.add(self.plane)

    def _on_window_delete(self, widget, data=None):
        self.hide_all()
        return True


class _PlaneWidget(gtk.DrawingArea, gtk.gtkgl.Widget):
    def __init__(self, source):
        gtk.DrawingArea.__init__(self)
        self._plane = None

        display_mode = (gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DOUBLE)
        try:
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        except gtk.gdkgl.NoMatches:            display_mode &= ~gtk.gdkgl.MODE_SINGLE
            glconfig = gtk.gdkgl.Config(mode = display_mode)

        self.set_gl_capability(glconfig)

        self.set_events(gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK|
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK|
                        gtk.gdk.BUTTON_PRESS_MASK |  gtk.gdk.SCROLL_MASK)

        self.connect( "expose_event", self._on_expose_event )
        self.connect( "realize", self._on_realize )
        self.connect( "configure_event", self._on_configure_event )
        
        self._roll = 0.0
        self._heading = 0.0
        self._pitch = 0.0
        
        if source:
            source.register_interest(self._on_ahrs, 10, "AHRS_EULER")

    def _on_ahrs(self, msg, payload):
        imu_phi, imu_theta, imu_psi, body_phi, body_theta, body_psi = msg.unpack_scaled_values(payload)

        #FIXME: we reverse the sign of roll here
        self.set_rotations(
                pitch=body_phi,
                roll=-body_theta,
                heading=0)

    def _cross_product(self, a, b):
        return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

    def _normalize(self, n):
        m = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        n[0] *= 1.0 / m
        n[1] *= 1.0 / m
        n[2] *= 1.0 / m

    def _on_configure_event(self, *args):
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        gldrawable.gl_begin(glcontext)
        w, h = self.get_gl_window().get_size()
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)   
        
        gldrawable.swap_buffers()
        gldrawable.gl_end()
        
    def _make_plane(self):
        self._plane = glGenLists(1)
        glNewList(self._plane, GL_COMPILE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_CULL_FACE)
        glBegin(GL_QUADS)

        path = os.path.join(os.path.dirname(__file__), "plane.raw")
        for line in file(path, 'r'):
            c = line.split(' ')
            c.remove(c[len(c)-1])
            c = map(float, c)

            n = self._cross_product(
                        [c[3]-c[0], c[4]-c[1], c[5]-c[2]],
                        [c[6]-c[0], c[7]-c[1], c[8]-c[2]])
            self._normalize(n)

            glNormal3d(n[0], n[1], n[2])
            glVertex3d(c[0], c[1], c[2])
            glVertex3d(c[3], c[4], c[5])
            glVertex3d(c[6], c[7], c[8])
            glVertex3d(c[9], c[10], c[11])
            
        glEnd()
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEndList()

    def _on_realize(self, *args):
        self._make_plane()

    def _on_expose_event(self, *args):
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        gldrawable.gl_begin(glcontext)
        
        w, h = self.get_gl_window().get_size()
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        self._display()

        gldrawable.swap_buffers()
        gldrawable.gl_end()
	        
    def _display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0,0.0,-11.0)
        
        glRotatef(20.0, 0.0, 1.0, 0.0)
        glRotatef(10.0, 1.0, 0.0, 0.0)
        glRotatef(self._roll, 1.0, 0.0, 0.0)
        glRotatef(self._heading, 0.0, 1.0, 0.0)
        glRotatef(self._pitch, 0.0, 0.0, 1.0)
        
        glCallList(self._plane)

        
    def set_rotations(self, pitch, roll, heading):
        self._pitch = pitch
        self._roll = roll
        self._heading = heading
        self.queue_draw()

if __name__ == "__main__":
    import random
    import gobject

    def rotate(pw):
        pw.set_rotations(
                2.0*random.random(),
                2.0*random.random(),
                0)
        return True

    p = PlaneView(None)
    p.show_all()

    gobject.timeout_add(1000/20,rotate, p.plane)

    gtk.main()

        	
