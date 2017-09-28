import sys
import unittest


from greedypacker import guillotine
from greedypacker import item
from .base import BaseTestCase
from .util import stdout_redirect


class FirstFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'first_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'first_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'first_fit')
        self.BIN.insert(ITEM2, 'first_fit')
        with self.subTest():
            correct = [self.freeRectangle(10, 3, 0, 2),
                        self.freeRectangle(4, 2, 6, 0)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three items
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'first_fit')
        self.BIN.insert(ITEM2, 'first_fit')
        self.BIN.insert(ITEM3, 'first_fit')
        with self.subTest():
            correct = [self.freeRectangle(4, 2, 6, 0),
                       self.freeRectangle(8, 2, 2, 2),
                       self.freeRectangle(10, 1, 0, 4)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
            self.assertEqual(ITEM3.CornerPoint, (0, 2))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class BestWidthFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(8, 4, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 9)
        self.assertFalse(self.BIN.insert(ITEM, 'best_width_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'best_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(4, 3, 4, 0),
                       self.freeRectangle(8, 1, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_width_fit')
        self.BIN.insert(ITEM2, 'best_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(8, 2, 0, 2),
                        self.freeRectangle(2, 2, 6, 0)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])



    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_width_fit')
        self.BIN.insert(ITEM2, 'best_width_fit')
        self.BIN.insert(ITEM3, 'best_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(8, 2, 0, 2)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
            self.assertEqual(ITEM3.CornerPoint, (6, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class BestHeightFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'best_height_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'best_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_height_fit')
        self.BIN.insert(ITEM2, 'best_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                        self.freeRectangle(8, 2, 2, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_height_fit')
        self.BIN.insert(ITEM2, 'best_height_fit')
        self.BIN.insert(ITEM3, 'best_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                        self.freeRectangle(6, 2, 4, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
            self.assertEqual(ITEM3.CornerPoint, (2, 3))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class BestAreaFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'best_area_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'best_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_area_fit')
        self.BIN.insert(ITEM2, 'best_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(10, 2, 0, 3),
                        self.freeRectangle(4, 2, 6, 0),
                        self.freeRectangle(6, 1, 4, 2)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(5, 1)
        self.BIN.insert(ITEM, 'best_area_fit')
        self.BIN.insert(ITEM2, 'best_area_fit')
        self.BIN.insert(ITEM3, 'best_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(10, 2, 0, 3),
                        self.freeRectangle(4, 2, 6, 0),
                        self.freeRectangle(1, 1, 9, 2)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
            self.assertEqual(ITEM3.CornerPoint, (4, 2))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class WorstWidthFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'worst_width_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'worst_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'worst_width_fit')
        self.BIN.insert(ITEM2, 'worst_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                        self.freeRectangle(8, 2, 2, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'worst_width_fit')
        self.BIN.insert(ITEM2, 'worst_width_fit')
        self.BIN.insert(ITEM3, 'worst_width_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                        self.freeRectangle(6, 2, 4, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
            self.assertEqual(ITEM3.CornerPoint, (2, 3))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class WorstHeightFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'worst_height_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'worst_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'worst_height_fit')
        self.BIN.insert(ITEM2, 'worst_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(10, 2, 0, 3),
                       self.freeRectangle(4, 2, 6, 0),
                       self.freeRectangle(6, 1, 4, 2)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'worst_height_fit')
        self.BIN.insert(ITEM2, 'worst_height_fit')
        self.BIN.insert(ITEM3, 'worst_height_fit')
        with self.subTest():
            correct = [self.freeRectangle(10, 2, 0, 3),
                       self.freeRectangle(6, 1, 4, 2),
                       self.freeRectangle(2, 2, 8, 0)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (4, 0))
            self.assertEqual(ITEM3.CornerPoint, (6, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


class WorstAreaFit(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)
        self.freeRectangle = guillotine.FreeRectangle


    def tearDown(self):
        del self.BIN
        del self.freeRectangle


    def testItemTooBig(self):
        """
        Single Item Fits no FreeRectangles
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(5, 11)
        self.assertFalse(self.BIN.insert(ITEM, 'worst_area_fit'))


    def testSingleItemInsertion(self):
        """
        Single item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        self.BIN.insert(ITEM, 'worst_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(10, 2, 0, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM])


    def testTwoItemInsertion(self):
        """
        Two item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'worst_area_fit')
        self.BIN.insert(ITEM2, 'worst_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(6, 3, 4, 0),
                       self.freeRectangle(8, 2, 2, 3)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2])


    def testThreeItemInsertion(self):
        """
        Three item
        Split Horizontal
        Rotation == False
        RectMerge == False
        """
        ITEM = item.Item(4, 3)
        ITEM2 = item.Item(2, 2)
        ITEM3 = item.Item(5, 1)
        self.BIN.insert(ITEM, 'worst_area_fit')
        self.BIN.insert(ITEM2, 'worst_area_fit')
        self.BIN.insert(ITEM3, 'worst_area_fit')
        with self.subTest():
            correct = [self.freeRectangle(8, 2, 2, 3),
                       self.freeRectangle(1, 1, 9, 0),
                       self.freeRectangle(6, 2, 4, 1)]
            self.assertEqual(self.BIN.freerects, correct)
        with self.subTest():
            self.assertEqual(ITEM.CornerPoint, (0, 0))
            self.assertEqual(ITEM2.CornerPoint, (0, 3))
            self.assertEqual(ITEM3.CornerPoint, (4, 0))
        with self.subTest():
            self.assertEqual(self.BIN.items, [ITEM, ITEM2, ITEM3])


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
        self.BIN.insert(ITEM, 'best_height_fit')
        self.BIN.insert(ITEM2, 'best_height_fit')
        self.assertEqual(self.BIN.freerects, [self.freeRectangle(6, 5, 4, 0)])


class BinStats(BaseTestCase):
    def setUp(self):
        self.BIN = guillotine.Guillotine(10, 5, rotation=False)


    def tearDown(self):
        del self.BIN


    def testReturn(self):
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(2, 2)
        self.BIN.insert(ITEM, 'best_width_fit')
        self.BIN.insert(ITEM2, 'best_width_fit')
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
        suite.addTests(loader.loadTestsFromTestCase(FirstFit))
        suite.addTests(loader.loadTestsFromTestCase(BestWidthFit))
        suite.addTests(loader.loadTestsFromTestCase(BestHeightFit))
        suite.addTests(loader.loadTestsFromTestCase(BestAreaFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstWidthFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstHeightFit))
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

