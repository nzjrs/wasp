import math
import gtk
import gtk.gtkgl

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

C_DEG2RAD = math.pi / 180.0

def drawText(msg):
    for c in msg:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(c))

def showMessage(x, y, msg, scale):
    glPushMatrix()
    glTranslatef( x, y, 0.0 )
    glScalef( 0.0001, 0.0001, 0.0001 )
    glScalef( scale, scale, scale )
    drawText( msg )
    glPopMatrix()

class HorizonView(gtk.Window):
    def __init__(self, source):
        gtk.Window.__init__(self)

        self.set_default_size(400, 400)
        self.set_title("Horizon View")
        self.connect("delete-event", self._on_window_delete)

        self.horizon = _HorizonWidget(source) 
        self.add(self.horizon)

    def _on_window_delete(self, widget, data=None):
        self.hide_all()
        return True

class _HorizonWidget(gtk.DrawingArea, gtk.gtkgl.Widget):
    def __init__(self, source):
        gtk.DrawingArea.__init__(self)
        
        glutInit()
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
        
        self._pitch = 0.0
        self._roll = 0.0
        self._yaw = 0.0
        self._speed = 0.0
        self._altitude = 0.0
        
        if source:
            source.register_interest(self._on_ahrs, 10, "AHRS_EULER")

    def _on_ahrs(self, msg, header, payload):
        imu_phi, imu_theta, imu_psi, body_phi, body_theta, body_psi = msg.unpack_scaled_values(payload)

        #FIXME: we reverse the sign of pitch here
        self.update(
                pitch=-body_phi,
                roll=body_theta,
                yaw=body_psi,
                altitude=0,
                speed=0)
        
    def _on_configure_event(self, *args):
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        gldrawable.gl_begin(glcontext)
        w, h = self.get_gl_window().get_size()
        if h == 0:
            h = 1
        glViewport( 0, 0, w, h )
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective(30.0, float(w)/float(h), 0.1, 2500.0)

        # select the Modelview matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()       
        gldrawable.swap_buffers()
        gldrawable.gl_end()

    def _on_realize(self, *args):
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        if not gldrawable.gl_begin(glcontext):
            return
            
        w, h = self.get_gl_window().get_size()
        
        glEnable(GL_CULL_FACE)
        glShadeModel(GL_FLAT)
        glClearColor(0.0, 0.0, 0.5, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(1.0)

        glViewport( 0, 0, w, h )
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective(30.0, float(w)/float(h), 0.1, 2500.0)

        # select the Modelview matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()

        self._display()
        
        gldrawable.gl_end()

    def _on_expose_event(self, *args):
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        gldrawable.gl_begin(glcontext)
        
        w, h = self.get_gl_window().get_size()
        if h == 0:
            h = 1
        
        glViewport( 0, 0, w, h )
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective(30.0, float(w)/float(h), 0.1, 2500.0)

        # select the Modelview matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        
        self._display()

        gldrawable.swap_buffers()
        gldrawable.gl_end()
	        
    def _display(self):

        headlabels = [
            "S",
            "19", "20", "21", "22", "23", "24", "25", "26",
            "W",
            "28", "29", "30", "31", "32", "33", "34", "35",
            "N",
            "1", "2", "3", "4", "5", "6", "7", "8",
            "E",
            "10", "11", "12", "13", "14", "15", "16", "17",
            "S"
        ]
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # ROLL TICK MARKS AND TICK MARKER **********/
        for n in xrange(-30, 31, 15):
            glPushMatrix()
            glRotatef(n, 0.0, 0.0, 1.0)
            glColor3f(1.0, 1.0, 1.0)
            glBegin( GL_LINES )
            glVertex3f(0.0, 0.24, -0.9)
            glVertex3f(0.0, 0.23, -0.9)
            glEnd()
            glPopMatrix()

        glPushMatrix()
        glRotatef(self._roll, 0.0, 0.0, 1.0)
        glColor3f(0.85, 0.5, 0.1)
        glBegin( GL_TRIANGLES )
        glVertex3f(0.0, 0.23, -0.9)
        glVertex3f(0.01, 0.21, -0.9)
        glVertex3f(-0.01, 0.21, -0.9)
        glEnd()
        glPopMatrix()


        # CENTER MARK ***********************/

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glBegin( GL_LINES )
        # right half
        glVertex3f(0.0, 0.0, -0.9)
        glVertex3f(0.015, -0.02, -0.9)

        glVertex3f(0.015, -0.02, -0.9)
        glVertex3f(0.03, 0.0, -0.9)

        glVertex3f(0.03, 0.0, -0.9)
        glVertex3f(0.06, 0.0, -0.9)
        # left half
        glVertex3f(0.0, 0.0, -0.9)
        glVertex3f(-0.015, -0.02, -0.9)

        glVertex3f(-0.015, -0.02, -0.9)
        glVertex3f(-0.03, 0.0, -0.9)

        glVertex3f(-0.03, 0.0, -0.9)
        glVertex3f(-0.06, 0.0, -0.9)
        glEnd()

        glPopMatrix()

        glRotatef(self._roll, 0.0, 0.0, 1.0)
        glTranslatef(-self._yaw*C_DEG2RAD, 0.0, 0.0)
        # HORIZON AND YAW TICK LINE **********/
        glColor3f(1.0, 1.0, 1.0)
        glBegin( GL_LINES )
        glVertex3f(-(180.0+15)*C_DEG2RAD, 0.0, -0.9)
        glVertex3f((180.0+15)*C_DEG2RAD, 0.0, -0.9)
        glEnd()

        for n in range(0,37):
            glBegin( GL_LINES )
            glVertex3f( float(n*10 - 180)*C_DEG2RAD, 0.015, -0.9)
            glVertex3f( float(n*10 - 180)*C_DEG2RAD, 0.0, -0.9)
            glEnd()
            glPushMatrix()
            glTranslatef(0.0, 0.0, -0.9)

            showMessage(float(n*10 - 180)*C_DEG2RAD-0.01,0.02,headlabels[n],1.2)
            
            glPopMatrix()

        # Extra tick mark past S (going W) for overview
        glBegin( GL_LINES )
        glVertex3f( 190.0*C_DEG2RAD, 0.02, -0.9)
        glVertex3f( 190.0*C_DEG2RAD, 0.0, -0.9)
        glEnd()
        glPushMatrix()
        glTranslatef(0.0, 0.0, -0.9)
        showMessage( 190.0*C_DEG2RAD-0.015, 0.02, "19\0", 1.0)
        glPopMatrix()
        # Extra tick mark past S (going E) for overview
        glBegin( GL_LINES )
        glVertex3f( -190.0*C_DEG2RAD, 0.02, -0.9)
        glVertex3f( -190.0*C_DEG2RAD, 0.0, -0.9)
        glEnd()
        glPushMatrix()
        glTranslatef(0.0, 0.0, -0.9)
        showMessage( -190.0*C_DEG2RAD-0.015, 0.02, "17\0", 1.0)
        glPopMatrix()


        glPushMatrix()
        glLoadIdentity()
        glRotatef(self._roll, 0.0, 0.0, 1.0)
        glTranslatef(0.0, -self._pitch*C_DEG2RAD, 0.0)

        # COLORED PART OF DISPLAY ************/
        glColor3f(0.0, 0.0, 1.0)
        glBegin( GL_QUADS )
        glVertex3f(-(180.0+15)*C_DEG2RAD, (90.0+15.0)*C_DEG2RAD, -1.0)
        glVertex3f((180.0+15)*C_DEG2RAD, (90.0+15.0)*C_DEG2RAD, -1.0)
        glVertex3f((180.0+15)*C_DEG2RAD, 0.0, -1.0)
        glVertex3f(-(180.0+15)*C_DEG2RAD, 0.0, -1.0)
        glEnd()

        # bottom of display
        glColor3f(0.5, 0.2, 0.1)
        glBegin( GL_QUADS )
        glVertex3f(-(180.0+15)*C_DEG2RAD, -(90.0+15.0)*C_DEG2RAD, -1.0)
        glVertex3f((180.0+15)*C_DEG2RAD, -(90.0+15.0)*C_DEG2RAD, -1.0)
        glVertex3f((180.0+15)*C_DEG2RAD, 0.0, -1.0)
        glVertex3f(-(180.0+15)*C_DEG2RAD, 0.0, -1.0)
        glEnd()

        # PITCH BARS *****************/
        for n in range(0,9):
            temp = float(n*10+10)*C_DEG2RAD
            glColor3f(1.0, 1.0, 1.0)
            # positive pitch lines
            glBegin( GL_LINES )
            glVertex3f(-0.1, temp-0.01, -1.0)
            glVertex3f(-0.1, temp, -1.0)

            glVertex3f(-0.1, temp, -1.0)
            glVertex3f(-0.03, temp, -1.0)

            glVertex3f(0.1, temp-0.01, -1.0)
            glVertex3f(0.1, temp, -1.0)

            glVertex3f(0.1, temp, -1.0)
            glVertex3f(0.03, temp, -1.0)

            glEnd()
            glPushMatrix()
            glTranslatef(0.0, 0.0, -1.0)
            showMessage(0.11, temp-0.007, str(n*10+10), 1.0)
            showMessage(-0.13, temp-0.007, str(n*10+10), 1.0)
            glPopMatrix()

            # negative pitch lines
            glBegin( GL_LINES )
            glVertex3f(-0.1, -temp+0.01, -1.0)
            glVertex3f(-0.1, -temp, -1.0)

            glVertex3f(-0.1, -temp, -1.0)
            glVertex3f(-0.03, -temp, -1.0)

            glVertex3f(0.1, -temp+0.01, -1.0)
            glVertex3f(0.1, -temp, -1.0)

            glVertex3f(0.1, -temp, -1.0)
            glVertex3f(0.03, -temp, -1.0)
            glEnd()
            glPushMatrix()
            glTranslatef(0.0, 0.0, -1.0)
            showMessage(0.11, -temp, str(n*10+10), 1.0)
            showMessage(-0.14, -temp, str(n*10+10), 1.0)
            glPopMatrix()

        # +/- 5 degree tick marks
        glBegin( GL_LINES )
        glVertex3f(-0.05, 5.0*C_DEG2RAD, -1.0)
        glVertex3f(0.05, 5.0*C_DEG2RAD, -1.0)
        glEnd()
        glBegin( GL_LINES )
        glVertex3f(-0.05, -5.0*C_DEG2RAD, -1.0)
        glVertex3f(0.05, -5.0*C_DEG2RAD, -1.0)
        glEnd()

        glPopMatrix()

        # BOUNDARY LINES ON EDGES AND ALITUTDE/SPEED READOUT ******************/
        glPushMatrix()
        glLoadIdentity()

        # altitude readout
        glColor3f(0.0, 1.0, 0.0)
        glPushMatrix()
        glTranslatef(-0.17, 0.140, -0.8)
        showMessage(-0.01, 0.0, "%3.2fm" % self._altitude, 1.0)
        glPopMatrix()

        # speed readout
        glPushMatrix()
        glTranslatef(0.12, 0.140, -0.8)
        showMessage(0.0, 0.0, "%3.2fk" % self._speed, 1.0)
        glPopMatrix()

        glPopMatrix()
        
    def update(self, pitch, roll, yaw, altitude, speed):
        self._pitch = pitch
        self._roll = roll
        self._yaw = yaw
        self._altitude = altitude
        self._speed = speed
        self.queue_draw()

if __name__ == "__main__":
    import random
    import gobject

    def rotate(hw):
        hw.update(
                pitch=10,
                roll=2.0*random.random(),
                yaw=0,
                altitude=100,
                speed=10)
        return True

    h = HorizonView(None)
    h.show_all()

    gobject.timeout_add(1000/20,rotate, h.horizon)

    gtk.main()
