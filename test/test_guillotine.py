import sys
import unittest

from sortedcontainers import SortedListWithKey
from greedypacker import guillotine
from greedypacker import item
from .base import BaseTestCase
from .util import stdout_redirect


class BestShortSide(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(8, 4, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle
        

    def tearDown(self):
        del self.BIN
        del self.freeRectangle

    
    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 9)
        self.assertFalse(self.BIN.best_shortside(ITEM))
        

    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(1, 2, 0, 0)
        F1 = self.freeRectangle(2, 2, 1, 0)
        ITEM = item.Item(1, 1)

        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.best_shortside(ITEM)

        with self.subTest():
            correct = [self.freeRectangle(1, 1, 0, 1),
                       self.freeRectangle(2, 2, 1, 0)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = SortedListWithKey([F0], key=lambda x: x.area, load=1000)
        self.BIN.best_shortside(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 30)


class BestLongSide(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.best_longside(ITEM))


    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(1, 3, 0, 0)
        F1 = self.freeRectangle(2, 1, 1, 0)
        ITEM = item.Item(1, 1)

        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.best_longside(ITEM)

        with self.subTest():
            correct = [self.freeRectangle(1, 3, 0, 0),
                       self.freeRectangle(1, 1, 2, 0)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 1)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 49)


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = [F0]
        self.BIN.best_longside(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 48)


class BestAreaFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'best_area_fit'))


    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 2, 0, 0)
        F1 = self.freeRectangle(3, 3, 2, 0)
        ITEM = item.Item(1, 1)
        
        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.best_area(ITEM)
        with self.subTest():
            correct = [self.freeRectangle(2, 1, 0, 1),
                        self.freeRectangle(1, 1, 1, 0),
                        self.freeRectangle(3, 3, 2, 0)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 49)


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = [F0]
        self.BIN.best_area(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 48)


class WorstLongSide(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(8, 4, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle
        

    def tearDown(self):
        del self.BIN
        del self.freeRectangle

    
    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 9)
        self.assertFalse(self.BIN.worst_shortside(ITEM))
        

    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(1, 3, 0, 0)
        F1 = self.freeRectangle(2, 1, 1, 0)
        ITEM = item.Item(1, 1)

        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.worst_longside(ITEM)

        with self.subTest():
            correct = [self.freeRectangle(1, 2, 0, 1),
                       self.freeRectangle(2, 1, 1, 0)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 31)


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = [F0]
        self.BIN.worst_longside(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 30)


class WorstShortSide(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(8, 4, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle
        

    def tearDown(self):
        del self.BIN
        del self.freeRectangle

    
    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 9)
        self.assertFalse(self.BIN.worst_shortside(ITEM))
        

    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(1, 2, 0, 0)
        F1 = self.freeRectangle(2, 2, 1, 0)
        ITEM = item.Item(1, 1)

        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.worst_shortside(ITEM)

        with self.subTest():
            correct = [self.freeRectangle(1, 2, 0, 0),
                       self.freeRectangle(2, 1, 1, 1),
                       self.freeRectangle(1, 1, 2, 0)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 1)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 31)


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = [F0]
        self.BIN.worst_shortside(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 30)


class WorstAreaFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemInsertionFailure(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'worst_area_fit'))


    def testItemInsertionSuccess(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 2, 0, 0)
        F1 = self.freeRectangle(3, 3, 2, 0)
        ITEM = item.Item(1, 1)
        
        self.BIN.freerects = SortedListWithKey([F0, F1], key=lambda x: x.area, load=1000)
        self.BIN.worst_area(ITEM)
        with self.subTest():
            correct = [self.freeRectangle(2, 2, 0, 0),
                        self.freeRectangle(2, 1, 3, 0),
                        self.freeRectangle(3, 2, 2, 1)]
            self.assertCountEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 2)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 49)


    def testItemInsertionSuccessRotation(self):
        """
        Single item
        Split Horizontal
        Rotation == True
        RectMerge == False
        """
        F0 = self.freeRectangle(2, 1, 0, 0)
        ITEM = item.Item(1, 2)
        
        self.BIN.rotation = True
        self.BIN.freerects = [F0]
        self.BIN.worst_area(ITEM)

        with self.subTest():
            self.assertCountEqual(self.BIN.freerects, [])
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])
        with self.subTest():
            self.assertEqual(self.BIN.free_area, 48)


class RectMerge(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle
        self.BIN.rMerge = True


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testMatchingWidths(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == True
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(4, 3)
        self.BIN.insert(ITEM, 'best_area')
        self.BIN.insert(ITEM2, 'best_area')
        self.assertEqual(self.BIN.freerects, [self.freeRectangle(6, 5, 4, 0)])


class BinStats(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)


    def tearDown(self):
        del self.BIN


    def testReturn(self):
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_area')
        self.BIN.insert(ITEM2, 'best_area')
        correct = {
            'width': 10,
            'height': 5,
            'area': 50,
            'efficiency': 0.24,
            'items': [ITEM, ITEM2],
            }

        self.assertEqual(self.BIN.bin_stats(), correct)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(BestShortSide))
        suite.addTests(loader.loadTestsFromTestCase(BestLongSide))
        suite.addTests(loader.loadTestsFromTestCase(BestAreaFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstShortSide))
        suite.addTests(loader.loadTestsFromTestCase(WorstLongSide))
        suite.addTests(loader.loadTestsFromTestCase(WorstAreaFit))
        suite.addTests(loader.loadTestsFromTestCase(RectMerge))
        suite.addTests(loader.loadTestsFromTestCase(BinStats))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite

