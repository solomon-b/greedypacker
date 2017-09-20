import sys
import unittest

import binpack

from .base import BaseTestCase
from .util import stdout_redirect

class APITests(BaseTestCase):
    def testReadme(self):
        """
        Example insertion from README.md
        """
        M = binpack.BinManager(8, 4, pack_algo='shelf')
        ITEM = binpack.Item(4, 2)
        ITEM2 = binpack.Item(5, 2)
        ITEM3 = binpack.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0,2))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (5,0))


class BestBinFit(BaseTestCase):
    def testGuillotineBWFSortingRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_width_fit)
        Item Sorting == True
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5, pack_algo='guillotine',
                               sorting=True, rotation=True)
        ITEM = binpack.Item(3, 4)
        ITEM2 = binpack.Item(5, 3)
        ITEM3 = binpack.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (5,0))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (0,3))

    def testGuillotineBWFRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_width_fit)
        Item Sorting == False
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5, pack_algo='guillotine',
                               sorting=False, rotation=True)
        ITEM = binpack.Item(3, 4)
        ITEM2 = binpack.Item(5, 3)
        ITEM3 = binpack.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (4,0))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (0,3))


    def testShelfBWFSortingRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == True
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5, pack_algo='shelf',
                               sorting=True, rotation=True)
        ITEM = binpack.Item(1, 1)
        ITEM2 = binpack.Item(4, 3)
        ITEM3 = binpack.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM3, ITEM]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (6,0))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (4,0))


    def testShelfBWFRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == False
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5, pack_algo='shelf',
                               sorting=False, rotation=True)
        ITEM = binpack.Item(1, 1)
        ITEM2 = binpack.Item(4, 3)
        ITEM3 = binpack.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (0,1))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (4,1))


class BinFirstFit(BaseTestCase):
    def testGuillotineBWFSortingRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_width_fit)
        Item Sorting == True
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5,
                               pack_algo='guillotine',
                               bin_algo="bin_first_fit",
                               sorting=True,
                               rotation=True)
        ITEM = binpack.Item(4, 3)
        ITEM2 = binpack.Item(6, 5)
        ITEM3 = binpack.Item(5, 5)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM3, ITEM]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (6,0))
        with self.subTest():
            self.assertEqual(ITEM2.CornerPoint, (0,0))
        with self.subTest():
            self.assertEqual(ITEM3.CornerPoint, (0,0))

    def testGuillotineBWFRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_width_fit)
        Item Sorting == False
        Item Rotation == True
        """
        M = binpack.BinManager(10, 5, pack_algo='guillotine',
                               sorting=False, rotation=True)
        ITEM = binpack.Item(4, 3)
        ITEM2 = binpack.Item(6, 5)
        #ITEM3 = binpack.Item(5, 5)
        M.add_items(ITEM, ITEM2)#, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2]#, ITEM3]
        #with self.subTest():
        #    self.assertEqual(M.items, correct)
        #with self.subTest():
        #    self.assertEqual(ITEM.CornerPoint, (0,0))
        #with self.subTest():
        #    self.assertEqual(ITEM2.CornerPoint, (4,0))
        #with self.subTest():
        #    self.assertEqual(ITEM3.CornerPoint, (0,0))


    #def testShelfBWFSortingRotation(self):
    #    """
    #    Best Bin Fit
    #    Shelf Bins (best_width_fit)
    #    Item Sorting == True
    #    Item Rotation == True
    #    """
    #    M = binpack.BinManager(10, 5, pack_algo='shelf',
    #                           sorting=True, rotation=True)
    #    ITEM = binpack.Item(1, 1)
    #    ITEM2 = binpack.Item(4, 3)
    #    ITEM3 = binpack.Item(2, 2)
    #    M.add_items(ITEM, ITEM2, ITEM3)
    #    M.execute()
    #    correct = [ITEM2, ITEM3, ITEM]
    #    with self.subTest():
    #        self.assertEqual(M.items, correct)
    #    with self.subTest():
    #        self.assertEqual(ITEM.CornerPoint, (6,0))
    #    with self.subTest():
    #        self.assertEqual(ITEM2.CornerPoint, (0,0))
    #    with self.subTest():
    #        self.assertEqual(ITEM3.CornerPoint, (4,0))


    #def testShelfBWFRotation(self):
    #    """
    #    Best Bin Fit
    #    Shelf Bins (best_width_fit)
    #    Item Sorting == False
    #    Item Rotation == True
    #    """
    #    M = binpack.BinManager(10, 5, pack_algo='shelf',
    #                           sorting=False, rotation=True)
    #    ITEM = binpack.Item(1, 1)
    #    ITEM2 = binpack.Item(4, 3)
    #    ITEM3 = binpack.Item(2, 2)
    #    M.add_items(ITEM, ITEM2, ITEM3)
    #    M.execute()
    #    correct = [ITEM, ITEM2, ITEM3]
    #    with self.subTest():
    #        self.assertEqual(M.items, correct)
    #    with self.subTest():
    #        self.assertEqual(ITEM.CornerPoint, (0,0))
    #    with self.subTest():
    #        self.assertEqual(ITEM2.CornerPoint, (0,1))
    #    with self.subTest():
    #        self.assertEqual(ITEM3.CornerPoint, (4,1))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(APITests))
        suite.addTests(loader.loadTestsFromTestCase(BestBinFit))
        suite.addTests(loader.loadTestsFromTestCase(BinFirstFit))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite
