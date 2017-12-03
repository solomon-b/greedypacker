import sys
import unittest

import greedypacker

from .base import BaseTestCase
from .util import stdout_redirect

class APITests(BaseTestCase):
    def testReadme(self):
        """
        Example insertion from README.md
        """
        M = greedypacker.BinManager(8, 4, pack_algo='shelf')
        ITEM = greedypacker.Item(4, 2)
        ITEM2 = greedypacker.Item(5, 2)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 2)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 5)
            self.assertEqual(ITEM3.y, 0)


class BestBinFit(BaseTestCase):
    def testGuillotineBWFSortingRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_area)
        Split Horizontal
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                                    pack_algo='guillotine',
                                    bin_algo="bin_best_fit",
                                    heuristic='best_area',
                                    sorting=True,
                                    rotation=True)
        ITEM = greedypacker.Item(4, 3)
        ITEM2 = greedypacker.Item(5, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 5)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 0)
            self.assertEqual(ITEM3.y, 3)


    def testNoSuchAlgo(self):
        with self.assertRaises(ValueError):
            M = greedypacker.BinManager(8, 4, pack_algo='foo')


    def testItemTooBig(self):
        M = greedypacker.BinManager(8, 4,
                                    pack_algo='skyline',
                                    bin_algo='bin_best_fit')
        I = greedypacker.Item(10,20)
        with self.assertRaises(ValueError):
            M.add_items(I)
            M.execute()
        

    def testShelfBigInsert(self):
        M = greedypacker.BinManager(2, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=True, rotation=True)

        I1 = greedypacker.item.Item(1, 1)
        I2 = greedypacker.item.Item(2, 1)
        I3 = greedypacker.item.Item(2, 2)
        M.add_items(*[I1,  I2, I3])
        M.execute()

        self.assertCountEqual(M.items, [I1, I2, I3])


    def testGuillotineBWFRotation(self):
        """
        Best Bin Fit
        Guillotine Bins (best_area)
        Split Horizontal
        Item Sorting == False
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                                    pack_algo='guillotine',
                                    bin_algo="bin_best_fit",
                                    heuristic='best_area',
                                    sorting=False,
                                    rotation=True)
        ITEM = greedypacker.Item(3, 4)
        ITEM2 = greedypacker.Item(5, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 3)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 8)
            self.assertEqual(ITEM3.y, 0)


    def testMaximalRectangleBSS(self):
        """
        Best Bin Fit
        Maximal Rectangle Bins (Best Short Side)
        Split Horizontal
        Item Sorting == False
        Item Rotation == False
        """
        M = greedypacker.BinManager(8, 4,
                                    pack_algo='maximal_rectangle',
                                    bin_algo="bin_best_fit",
                                    heuristic='best_shortside',
                                    sorting=False,
                                    rotation=False)

        I = greedypacker.Item(1, 1)
        I2 = greedypacker.Item(2, 2)
        F0 = greedypacker.maximal_rectangles.FreeRectangle(7, 1, 1, 0)
        F1 = greedypacker.maximal_rectangles.FreeRectangle(8, 1, 0, 3)
        F2 = greedypacker.maximal_rectangles.FreeRectangle(6, 4, 2, 0)
        M.add_items(I, I2)
        M.execute()
        with self.subTest():
            self.assertCountEqual(M.bins[0].freerects, [F0, F1, F2])
        with self.subTest():
            self.assertEqual(I.x, 0)
            self.assertEqual(I.y, 0)
        with self.subTest():
            self.assertEqual(I2.x, 0)
            self.assertEqual(I2.y, 1)


    def testShelfBWFSortingRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                                    pack_algo='shelf',
                                    bin_algo="bin_best_fit",
                                    heuristic='best_width_fit',
                                    sorting=True,
                                    rotation=True)
        ITEM = greedypacker.Item(1, 1)
        ITEM2 = greedypacker.Item(4, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM3, ITEM]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 6)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 4)
            self.assertEqual(ITEM3.y, 0)


    def testShelfBWFRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == False
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                                    pack_algo='shelf',
                                    bin_algo="bin_best_fit",
                                    heuristic='best_width_fit',
                                    sorting=False,
                                    rotation=True)
        ITEM = greedypacker.Item(1, 1)
        ITEM2 = greedypacker.Item(4, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 1)
        with self.subTest():
            self.assertEqual(ITEM3.x, 4)
            self.assertEqual(ITEM3.y, 1)


    def testSkyline(self):
        """
        Bin Best Fit
        Skyline (bottom_left)
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='skyline',
                               bin_algo="bin_best_fit",
                               sorting=True,
                               rotation=True)

        ITEM = greedypacker.Item(10, 3)
        ITEM2 = greedypacker.Item(10, 4)
        ITEM3 = greedypacker.Item(1, 1)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertCountEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 0)
            self.assertEqual(ITEM3.y, 3)


class BinFirstFit(BaseTestCase):
    def testGuillotineBWFSortingRotation(self):
        """
        Bin First Fit
        Guillotine Bins (best_width_fit)
        Split Horizontal
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='guillotine',
                               heuristic='best_area',
                               bin_algo="bin_first_fit",
                               sorting=True,
                               rotation=True)
        ITEM = greedypacker.Item(4, 3)
        ITEM2 = greedypacker.Item(6, 5)
        ITEM3 = greedypacker.Item(5, 5)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM3, ITEM]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 6)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 0)
            self.assertEqual(ITEM3.y, 0)


    def testGuillotineBWFRotation(self):
        """
        Bin First Fit
        Guillotine Bins (best_width_fit)
        Split Horizontal
        Item Sorting == False
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='guillotine',
                               heuristic='best_area',
                               bin_algo="bin_first_fit",
                               sorting=False,
                               rotation=True)
        ITEM = greedypacker.Item(4, 3)
        ITEM2 = greedypacker.Item(6, 5)
        ITEM3 = greedypacker.Item(4, 4)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 6)
            self.assertEqual(ITEM3.y, 0)


    def testShelfBWFSortingRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='shelf',
                               heuristic='best_width_fit',
                               bin_algo="bin_first_fit",
                               sorting=True,
                               rotation=True)
        ITEM = greedypacker.Item(1, 1)
        ITEM2 = greedypacker.Item(4, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM2, ITEM3, ITEM]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 6)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 4)
            self.assertEqual(ITEM3.y, 0)


    def testShelfBWFRotation(self):
        """
        Best Bin Fit
        Shelf Bins (best_width_fit)
        Item Sorting == False
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='shelf',
                               bin_algo="bin_first_fit",
                               sorting=False,
                               rotation=True)
        ITEM = greedypacker.Item(1, 1)
        ITEM2 = greedypacker.Item(4, 3)
        ITEM3 = greedypacker.Item(2, 2)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 1)
        with self.subTest():
            self.assertEqual(ITEM3.x, 4)
            self.assertEqual(ITEM3.y, 1)

    def testShelfBWFRotationIdenticalItems(self):
        """
        Manually insert two identical items
        """
        ITEM = greedypacker.Item(1, 2)
        ITEM2 = greedypacker.Item(1, 2)
        M = greedypacker.BinManager(10, 5,
                               pack_algo='shelf',
                               bin_algo='bin_first_fit',
                               heuristic='best_width_fit',
                               sorting_heuristic='ASCA',
                               rotation=True)
        M.add_items(ITEM, ITEM2)
        M.execute()
        #print(M.bins)
        #self.assertCountEqual(M.bins[0].items, [ITEM, ITEM2])


    def testSkyline(self):
        """
        Bin First Fit
        Skyline (bottom_left)
        Item Sorting == True
        Item Rotation == True
        """
        M = greedypacker.BinManager(10, 5,
                               pack_algo='skyline',
                               bin_algo="bin_first_fit",
                               sorting=True,
                               rotation=True)

        ITEM = greedypacker.Item(10, 3)
        ITEM2 = greedypacker.Item(10, 4)
        ITEM3 = greedypacker.Item(1, 1)
        M.add_items(ITEM, ITEM2, ITEM3)
        M.execute()
        correct = [ITEM, ITEM2, ITEM3]
        with self.subTest():
            self.assertCountEqual(M.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(ITEM3.x, 0)
            self.assertEqual(ITEM3.y, 4)


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
