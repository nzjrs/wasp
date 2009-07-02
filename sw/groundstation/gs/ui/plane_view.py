import math
import os.path
import gtk.gtkgl

from OpenGL.GL import *
from OpenGL.GLU import *

class PlaneView(gtk.DrawingArea, gtk.gtkgl.Widget):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
        self.win = gtk.Window()
        
        self.plane = None

        self.set_events(gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK|
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK|
                        gtk.gdk.BUTTON_PRESS_MASK |  gtk.gdk.SCROLL_MASK)

        display_mode = (gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DOUBLE)

        try:
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        except gtk.gdkgl.NoMatches:            display_mode &= ~gtk.gdkgl.MODE_SINGLE
            glconfig = gtk.gdkgl.Config(mode = display_mode)

        self.set_gl_capability(glconfig)

        self.set_events(gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK|
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK|
                        gtk.gdk.BUTTON_PRESS_MASK |  gtk.gdk.SCROLL_MASK)

        self.connect( "expose_event", self.on_expose_event )
        self.connect( "realize", self.on_realize )
        self.connect( "configure_event", self.on_configure_event )
        
        self.win.connect("delete-event", self.on_window_delete)

        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        
        self.win.add(self)
        self.win.set_default_size(500, 400)
        self.win.set_title("Plane View")

    def _cross_product(self, a, b):
        return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

    def _normalize(self, n):
        m = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        n[0] *= 1.0 / m
        n[1] *= 1.0 / m
        n[2] *= 1.0 / m

    def on_window_delete(self, widget, data=None):
        self.win.hide_all()
        return True
        
    def show_all(self):
        self.win.show_all()      

    def on_configure_event(self, *args):
        #print "configure"
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
        
    def make_plane(self):
        self.plane = glGenLists(1)
        glNewList(self.plane, GL_COMPILE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_CULL_FACE)
        glBegin(GL_QUADS)

        path = os.path.join(os.path.dirname(__file__), "plane.raw")
        for line in file(path):
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

    def on_realize(self,*args):
        #print "realise"
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        if not gldrawable.gl_begin(glcontext):
            return
            
        w, h = self.get_gl_window().get_size()

        self.make_plane()
                    
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_BLEND)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.5,0.5,1.0,0)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0,float(w)/float(h),0.1,100.0)
        glMatrixMode(GL_MODELVIEW)
       
        self.display()
        
        gldrawable.gl_end()

    def on_expose_event(self, *args):
        #print "expose"
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        gldrawable.gl_begin(glcontext)
        
        w, h = self.get_gl_window().get_size()
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_BLEND)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        self.display()

        gldrawable.swap_buffers()
        gldrawable.gl_end()
	        
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0,0.0,-11.0)
        
        glRotatef(20.0, 0.0, 1.0, 0.0)
        glRotatef(10.0, 1.0, 0.0, 0.0)
        glRotatef(self.pitch, 1.0, 0.0, 0.0)
        glRotatef(self.yaw, 0.0, 1.0, 0.0)
        glRotatef(self.roll, 0.0, 0.0, 1.0)
        
        glCallList(self.plane)
        
    def set_rotations(self, pitch, yaw, roll):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.queue_draw()

        	
