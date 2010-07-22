import unittest

import gs

class UtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def testScaleToRange(self):
        self.failUnlessAlmostEqual(
                gs.scale_to_range(5.0,oldrange=(0.0,10.0),newrange=(0.0, 1.0)), 0.5, places=2)
        self.failUnlessAlmostEqual(
                gs.scale_to_range(0.0,(-5.0,5.0),newrange=(0.0, 1.0)), 0.5, places=2)
        self.failUnlessAlmostEqual(
                gs.scale_to_range(0.0,oldrange=(-32767,32767),newrange=(-9600,9600)), 0.0, places=2)
        self.failUnlessAlmostEqual(
                gs.scale_to_range(7.5,oldrange=(5.0,10.0),newrange=(0.0,5.0)), 2.5, places=2)


if __name__ == "__main__":
    unittest.main()
