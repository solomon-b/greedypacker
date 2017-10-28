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
        F = maximal_rectangles.FreeRectangle(2, 3, 0, 0)

        self.assertFalse(self.M.item_fits_rect(I, F))

    
    def testSplitRectangle(self):
        """
        Split a rectangle into two maximal rectangles
        """
        I = item.Item(2,2)
        F = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        
        Ft = maximal_rectangles.FreeRectangle(4, 2, 0, 2)
        Fr = maximal_rectangles.FreeRectangle(2, 4, 2, 0)

        remainders = self.M.split_rectangle(F, I)
        self.assertCountEqual(remainders, [Ft, Fr])
        

    def testCheckIntersectionTrue(self):
        """
        Two items with partial overlap
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        B = (0, 0, 2, 2)
        self.assertTrue(self.M.checkInstersection(F0, B))


    def testCheckIntersectionFalse(self):
        """
        Two items with no overlap
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        B = (5, 0, 9, 2)
        self.assertFalse(self.M.checkInstersection(F0, B))


    def testItemBounds(self):
        """
        Returns the bounding box for an item
        """
        I = item.Item(4, 2, [2,1])
        self.assertEqual(self.M.item_bounds(I), (2, 1, 6, 3))
    

    def testFindOverlap(self):
        """
        Returns the area of overlap of two
        intersected rectangles
        """
        F0 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(4, 2, 3, 0)
        B = (3, 0, 7, 2)

        self.assertEqual(self.M.findOverlap(F0, B), (3, 0, 4, 2))


    def testClipOverlap(self):
        """
        Returns maximal rectangle remainders of a rectangle
        fully overlapping a bounding box
        """
        F0 = maximal_rectangles.FreeRectangle(3, 3, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(1, 1, 1, 1)
        B = (1, 1, 2, 2)
    
        overlap = self.M.findOverlap(F0, B)
        remainders = self.M.clipOverlap(F0, overlap)

        Fl = maximal_rectangles.FreeRectangle(1, 3, 0, 0)
        Fr = maximal_rectangles.FreeRectangle(1, 3, 2, 0)
        Fb = maximal_rectangles.FreeRectangle(3, 1, 0, 0)
        Ft = maximal_rectangles.FreeRectangle(3, 1, 0, 2)

        self.assertCountEqual(remainders, [Fl, Fr, Fb, Ft])
        

    def testEncapsulates(self):
        """
        Returns a boolean if the second rectangle
        is fully encapsulated in the first
        """
        F0 = maximal_rectangles.FreeRectangle(3, 3, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(1, 1, 1, 1)
        F2 = maximal_rectangles.FreeRectangle(2, 1, 5, 1)

        with self.subTest():
            self.assertTrue(self.M.encapsulates(F0, F1))
        with self.subTest():
            self.assertFalse(self.M.encapsulates(F0, F2))


    def testRemoveRedundent(self):
        """
        F1 should be removed from freerects
        """
        F0 = maximal_rectangles.FreeRectangle(3, 3, 0, 0)
        F1 = maximal_rectangles.FreeRectangle(1, 1, 1, 1)
        F2 = maximal_rectangles.FreeRectangle(2, 1, 5, 1)
        F3 = maximal_rectangles.FreeRectangle(1, 1, 5, 1)
        self.M.freerects = [F0, F1, F2, F3]
        self.M.remove_redundent()
        self.assertCountEqual(self.M.freerects, [F0, F2])


class FirstFit(BaseTestCase):
    def setUp(self):
        self.M = maximal_rectangles.MaximalRectangle(4, 4)


    def tearDown(self):
        del self.M


    def testSingleItemInsert(self):
        """
        Single Item insertion checks for maximal
        rectangles result
        """
        I = item.Item(2, 2)
        F0 = maximal_rectangles.FreeRectangle(2, 4, 2, 0)
        F1 = maximal_rectangles.FreeRectangle(4, 2, 0, 2)
        self.M.first_fit(I)
        self.assertCountEqual(self.M.freerects, [F0, F1])


    def testTwoItemInsert(self):
        """
        Two Item insertion checks for maximal
        rectangles result
        """
        I = item.Item(2, 2)
        I2 = item.Item(4, 2)
        self.M.first_fit(I)
        self.M.first_fit(I2)
        F0 = maximal_rectangles.FreeRectangle(2, 2, 2, 0)
        self.assertEqual(self.M.freerects, [F0])


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(StaticMethods))
        suite.addTests(loader.loadTestsFromTestCase(FirstFit))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite


