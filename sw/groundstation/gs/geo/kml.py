#-----------------------------------------------------------------------------
# Communicate w/ a Decathlon Keymaze 500/700 devices
#-----------------------------------------------------------------------------
# @author Emmanuel Blot <manu.blot@gmail.com> (c) 2009
# @license MIT License, see LICENSE file
#-----------------------------------------------------------------------------

import xml.etree.ElementTree as ET

class KmlDoc(object):
    """Importer/Exporter for Google KML file format
    """
    def __init__(self, name):
        self.linestyles = {}
        self.root = ET.Element('kml')
        self.root.set('xmlns', 'http://www.opengis.net/kml/2.2')
        self.doc = ET.SubElement(self.root, 'Document')
        self.placemark = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(self.placemark, 'name').text = name
        
    def _add_linestyle(self, **kwargs):
        sid = '_'.join(['%s%s' % (k,v) for (k,v) in kwargs.items()])
        if sid not in self.linestyles:
            self.linestyles[sid] = kwargs.copy()
        return sid
        
    def add_trackpoints(self, geopoints, zoffset=0, extrude=True, tessellate=True):
        if isinstance(geopoints, tuple):
            geopoints = [geopoints]
        ET.SubElement(self.placemark, 'styleUrl').text = '#%s' % \
            self._add_linestyle(color='7f7f00ff', width='8')
        ls = ET.SubElement(self.placemark, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude and '1' or '0'
        ET.SubElement(ls, 'tessellate').text = tessellate and '1' or '0'
        ET.SubElement(ls, 'altitudeMode').text = 'absolute'
        coord = ET.SubElement(ls, 'coordinates')
        coord.text = '\n'.join([','.join(map(str, 
                                             (g.lon,g.lat,g.alt+zoffset))) \
                                    for g in geopoints])
            
    def write(self, out):
        out.write('<?xml version="1.0" encoding="UTF-8"?>')
        for (sid, props) in self.linestyles.items():
            style = ET.SubElement(self.doc, 'Style')
            style.set('id', sid)
            linestyle = ET.SubElement(style, 'LineStyle')
            for (k,v) in props.items():
                ET.SubElement(linestyle, k).text = v
        out.write(ET.tostring(self.root))

if __name__== "__main__":
    import StringIO

    f = StringIO.StringIO()
    k = KmlDoc("test")

    points = [(-50.1,34,2000),(-50.1,34,2000),(-50.11,34,2000),(-50.12,34,2020),(-50.12,34,2050)]

    k.add_trackpoints(points)
    k.write(f)

    print f.getvalue()
