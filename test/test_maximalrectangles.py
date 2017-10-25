import sys
import unittest


from greedypacker import maximal_rectangles
from greedypacker import item
from .base import BaseTestCase
from .util import stdout_redirect


class StaticMethods(BaseTestCase):
    def setUp(self):
        self.M = maximal_rectangles.MaximalRectangle(0, 0)


    def tearDown(self):
        del self.M


    def testItemFitsRect(self):
        """
        Single Item Fits the FreeRectangle
        Rotation == False
        """
        I = item.Item(2, 4)
        F = maximal_rectangles.FreeRectangle(2, 4, 0 ,0)

        self.assertTrue(self.M.item_fits_rect(I, F))


    def testItemDoesntFitsRect(self):
        """
        Single Item Fits the FreeRectangle
        Rotation == False
        """
        I = item.Item(2, 4)
        F = maximal_rectangles.FreeRectangle(2, 3, 0 ,0)

        self.assertFalse(self.M.item_fits_rect(I, F))


    def testCheckIntersectionTrue(self):
        """
        Two items with partial overlap
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(4, 2, 0, 0)

        self.assertTrue(self.M.checkInstersection(F0, F1))


    def testCheckIntersectionFalse(self):
        """
        Two items with no overlap
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(4, 2, 5, 0)

        self.assertFalse(self.M.checkInstersection(F0, F1))

    
    def testFindOverlap(self):
        """
        Returns the area of overlap of two
        intersected rectangles
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(4, 2, 3, 0)

        self.assertEqual(self.M.findOverlap(F0, F1), (3, 0, 4, 2))


    def testClipOverlap(self):
        """
        Returns maximal rectangle remainders of a rectangle
        fully overlapping another rectangle
        """
        F0 = maximal_rectangles.FreeRectangle(3, 3, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(1, 1, 1, 1)

        overlap = self.M.findOverlap(F0, F1)
        remainders = self.M.clipOverlap(F0, overlap)

        Fl = maximal_rectangles.FreeRectangle(1, 3, 0, 0)
        Fr = maximal_rectangles.FreeRectangle(1, 3, 2, 0)
        Fb = maximal_rectangles.FreeRectangle(3, 1, 0, 0)
        Ft = maximal_rectangles.FreeRectangle(3, 1, 0, 2)

        self.assertCountEqual(remainders, [Fl, Fr, Fb, Ft])


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(StaticMethods))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite


