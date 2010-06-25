import unittest

import gs

class UtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def testScaleToRange(self):
        self.failUnlessAlmostEqual(
                gs.scale_to_range(5.0,(0.0,10.0)), 0.5, places=2)
        self.failUnlessAlmostEqual(
                gs.scale_to_range(0.0,(-5.0,5.0)), 0.5, places=2)

if __name__ == "__main__":
    unittest.main()
