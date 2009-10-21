import unittest

import gs.geo as geo

class DistanceTest(unittest.TestCase):
    def setUp(self):
        #co-ordinates from
        #http://www.travelmath.com/airport/LAX
        #http://www.travelmath.com/airport/BNA
        lax = (33.9425222, -118.4071611)
        bna = (36.12666666, -86.68194444)
        lax_bna_dist = 2892220.95684

        #co-ordinates from
        #http://pyroms.googlecode.com/svn/trunk/pyroms/greatcircle.py
        #ellipsoidal distance should be 54972.271m
        flinders_peak = (-37.951033, 144.424868)
        buninyon = (-37.652821, 143.926496)
        flinders_buninyon_dist = 54972.271

        self._testdata = (
            (lax, bna, "lax->bna", lax_bna_dist),
            (flinders_peak, buninyon, "flinders peak->buninyon", flinders_buninyon_dist)
        )

    def testVinchey(self):
        for start,end,name,answer in self._testdata:
            d = geo.crow_flies_distance_two_point(start, end, "vinchey")
            self.failUnlessAlmostEqual(d, answer, places=1)

if __name__ == "__main__":
    unittest.main()


