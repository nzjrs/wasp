#http://www2.warwick.ac.uk/fac/sci/csc/people/computingstaff/jaroslaw_zachwieja/gegpsd

import gtk
import os.path
import logging
import subprocess

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('gevis')

class GoogleEarthVis(plugin.Plugin):

    EXECUTABLE = "googleearth"

    def __init__(self, conf, source, messages_file, groundstation_window):
        if not gs.utils.program_installed(self.EXECUTABLE):
            raise plugin.PluginNotSupported("%s not installed" % self.EXECUTABLE)

        pb = gs.ui.get_icon_pixbuf("world.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Show Flight in Google Earth")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._start_google_earth)
        groundstation_window.add_menu_item("Window", item)

        #register interest in the GPS_LLH messags
        source.register_interest(self._on_gps, 0, "GPS_LLH")

        self._file = "/tmp/wasp-realtime.kml"
        self._got_gps = False
        self._process = None

    def _write_kml(self, lat, lon, alt, heading, speed):
        speed = int(speed * 1.852)
        range_ = ( ( speed / 100  ) * 350 ) + 650
        tilt = ( ( speed / 120 ) * 43 ) + 30

        if speed < 10:
            range_ = 200
            tilt = 30
            heading = 0

        output = """<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://earth.google.com/kml/2.0">
            <Placemark>
                <name>%s km/h</name>
                <description>^</description>
                <LookAt>
                    <longitude>%s</longitude>
                    <latitude>%s</latitude>
                    <range>%s</range>
                    <tilt>%s</tilt>
                    <heading>%s</heading>
                </LookAt>
                <Point>
                    <coordinates>%s,%s,%s</coordinates>
                </Point>
            </Placemark>
        </kml>""" % (speed,lon,lat,range_,tilt,heading,lon,lat,alt)

        f=open(self._file, 'w')
        f.write(output)
        f.close()

    def _on_gps(self, msg, header, payload):
        fix,sv,lat,lon,hsl,hacc,vacc = msg.unpack_scaled_values(payload)

        #convert from mm to m
        hsl = hsl/1000.0

        if fix:
            self._write_kml(lat, lon, hsl, 0, 8)

    def _start_google_earth(self, *args):
        #write the kml file that references the dynamic kml
        #file the always contains the location of the UAV
        kml = "/tmp/wasp.kml"
        output = """<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://earth.google.com/kml/2.2">
        <NetworkLink>
            <name>Realtime GPS</name>
            <open>1</open>
            <Link>
	            <href>%s</href>
	            <refreshMode>onInterval</refreshMode>
            </Link>
        </NetworkLink>
        </kml>""" % self._file
        f=open(kml, 'w')
        f.write(output)
        f.close()

        #start googleearth
        self._process = subprocess.Popen(
                            "%s %s" % (self.EXECUTABLE, kml),
                            shell=True,
                            stdout=None,
                            stderr=None)

