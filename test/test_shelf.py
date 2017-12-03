import sys
import unittest

from greedypacker import shelf
from greedypacker import item

from .base import BaseTestCase
from .util import stdout_redirect

class WasteMap(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4, rotation=True, wastemap=True)


    def tearDown(self):
        del self.sheet


    def testAddToWastemapA(self):
        """
       Manual Triggering of sheet.add_to_wastmap
        Without vertical offest
        """
        self.sheet.use_waste_map = False

        ITEM1 = item.Item(3,3)
        ITEM2 = item.Item(2,2)
        ITEM3 = item.Item(2,2)

        self.sheet.insert(ITEM1, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        self.sheet.insert(ITEM3, heuristic='next_fit')
        self.sheet.add_to_wastemap(self.sheet.shelves[-1])

        correct = [(1, 3, 7, 0), (4, 1, 3, 2)]
        self.assertEqual(self.sheet.wastemap.freerects, correct)


    def testAddToWastemapB(self):
        """
        Manual Triggering of sheet.add_to_wastmap
        With vertical offest
        """
        self.sheet.use_waste_map = False

        ITEM0 = item.Item(8,1)
        ITEM1 = item.Item(3,3)
        ITEM2 = item.Item(2,2)
        ITEM3 = item.Item(2,2)

        self.sheet.insert(ITEM0, heuristic='next_fit')
        self.sheet.insert(ITEM1, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        self.sheet.insert(ITEM3, heuristic='next_fit')
        self.sheet.add_to_wastemap(self.sheet.shelves[-1])

        correct = [(1, 3, 7, 1), (4, 1, 3, 3)]
        self.assertEqual(self.sheet.wastemap.freerects, correct)


    def testAddAnItemToWasteMap(self):
        """
        Waste Map generation and insertion using shelf.insert()
        """
        self.sheet.use_waste_map = True

        ITEM0 = item.Item(8,1)
        ITEM1 = item.Item(3,3)
        ITEM2 = item.Item(2,2)
        ITEM3 = item.Item(3,3)
        ITEM4 = item.Item(1,2)

        self.sheet.insert(ITEM0, heuristic='next_fit')
        self.sheet.insert(ITEM1, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        self.sheet.insert(ITEM3, heuristic='next_fit')
        self.sheet.insert(ITEM4, heuristic='next_fit')

        with self.subTest():
            self.assertEqual(self.sheet.items, [ITEM0, ITEM1, ITEM2, ITEM3, ITEM4])
        with self.subTest():
            self.assertEqual(self.sheet.wastemap.freerects, [])


class shelfObject(BaseTestCase):
    def setUp(self):
        self.shelf = shelf.Shelf(8,4, 0)

    def tearDown(self):
        del self.shelf

    def testInsertOnce(self):
        """
        Manual insertion into a shelf object
        """
        ITEM = item.Item(4, 2)
        self.shelf.insert(ITEM)
        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.shelf.items, correct)
        with self.subTest():
            correct = 4
            self.assertEqual(self.shelf.available_width, correct)


    def testInsertTwice(self):
        """
        Manual insertion into a shelf object twice
        """
        ITEM = item.Item(4, 2)
        self.shelf.insert(ITEM)
        self.shelf.insert(ITEM)
        with self.subTest():
            correct = [ITEM, ITEM]
            self.assertEqual(self.shelf.items, correct)
        with self.subTest():
            correct = 0
            self.assertEqual(self.shelf.available_width, correct)


    def testInsertTwoIdenticalItems(self):
        """
        Manually insert two identical items
        """
        ITEM = item.Item(1, 2)
        ITEM2 = item.Item(1, 2)
        self.shelf.insert(ITEM)
        self.shelf.insert(ITEM2)
        self.assertCountEqual(self.shelf.items, [ITEM, ITEM2])


    def testItemTooWide(self):
        """
        Manual insertion of oversized (width) object into a shelf
        """
        ITEM = item.Item(9, 2)
        result = self.shelf.insert(ITEM)
        with self.subTest():
            self.assertEqual(self.shelf.items, [])
        with self.subTest():
            self.assertFalse(result)


    def testItemTooTall(self):
        """
        Manual insertion of oversized (height) object into a shelf
        """
        ITEM = item.Item(6, 5)
        result = self.shelf.insert(ITEM)
        with self.subTest():
            self.assertEqual(self.shelf.items, [])
        with self.subTest():
            self.assertFalse(result)


class NextFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)
        self.sheet.rotation = True

    def tearDown(self):
        del self.sheet

    def testSingleInsert(self):
        """
        Single item insertion
        """
        ITEM = item.Item(6, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        with self.subTest():
            correct= [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)


    def testTwoInsertsA(self):
        """
        Two items that fit in one shelf
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(3, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
            self.assertEqual(ITEM.width, 3)
            self.assertEqual(ITEM.height, 2)
            self.assertEqual(ITEM2.x, 3)
            self.assertEqual(ITEM2.y, 0)
            self.assertEqual(ITEM2.width, 3)
            self.assertEqual(ITEM2.height, 2)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 20)


    def testTwoInsertsB(self):
        """
        Two items that fit in two shelves
        """
        ITEM = item.Item(2, 2)
        ITEM2 = item.Item(7, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 2)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 14)


    def testTwoInsertsC(self):
        """
        Second item doesn't fit remaining vertical space in sheet
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(7, 3)
        self.sheet.insert(ITEM, heuristic='next_fit')
        res = self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertFalse(res)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 26)


    def testTwoInsertsD(self):
        """
        Manually insert two identical items
        """
        ITEM = item.Item(1, 2)
        ITEM2 = item.Item(1, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        self.assertCountEqual(self.sheet.items, [ITEM, ITEM2])


class NextFitNoRotation(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)
        self.sheet.rotation = False

    def tearDown(self):
        del self.sheet

    def testSingleInsert(self):
        """
        Single item insertion
        """
        ITEM = item.Item(6, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 20)


    def testTwoInsertsA(self):
        """
        Two items that fit in one shelf
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(3, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
            self.assertEqual(ITEM.width, 3)
            self.assertEqual(ITEM.height, 2)
            self.assertEqual(ITEM2.x, 3)
            self.assertEqual(ITEM2.y, 0)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 20)


    def testTwoInsertsB(self):
        """
        Two items that fit in two shelves
        """
        ITEM = item.Item(2, 2)
        ITEM2 = item.Item(7, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
            self.assertEqual(ITEM2.x, 0)
            self.assertEqual(ITEM2.y, 2)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 14)


    def testTwoInsertsC(self):
        """
        Second item doesn't fit remaining vertical space in sheet
        """
        ITEM = item.Item(7, 3)
        ITEM2 = item.Item(3, 2)
        self.sheet.insert(ITEM, heuristic='next_fit')
        res = self.sheet.insert(ITEM2, heuristic='next_fit')
        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertFalse(res)
        with self.subTest():
            self.assertEqual(ITEM.x, 0)
            self.assertEqual(ITEM.y, 0)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 11)


class FirstFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testSingleInsert(self):
        """
        Single item insertion doesn't use a heuristic
        """
        ITEM = item.Item(6, 2)
        self.sheet.insert(ITEM, heuristic='first_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)

        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 20)


    def testTwoInsertsA(self):
        """
        Two items that fit in one shelf
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(3, 2)
        self.sheet.insert(ITEM, heuristic='first_fit')
        self.sheet.insert(ITEM2, heuristic='first_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            correct.insert(ITEM2)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 20)


    def testTwoInsertsB(self):
        """
        Two items that fit in two shelves
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(6, 2)
        self.sheet.insert(ITEM, heuristic='first_fit')
        self.sheet.insert(ITEM2, heuristic='first_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 14)


    def testTwoInsertsC(self):
        """
        Second item doesn't fit remaining vertical space in sheet
        """
        ITEM = item.Item(3, 2)
        ITEM2 = item.Item(6, 3)
        self.sheet.insert(ITEM, heuristic='first_fit')
        res = self.sheet.insert(ITEM2, heuristic='first_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            self.assertFalse(res)
        with self.subTest():
            correct = [ITEM]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 26)


    def testThreeInsertsA(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(5, 2)
        ITEM2 = item.Item(4, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='first_fit')
        self.sheet.insert(ITEM2, heuristic='first_fit')
        self.sheet.insert(ITEM3, heuristic='first_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            correct.insert(ITEM3)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)



class BestWidthFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='best_width_fit')
        self.sheet.insert(ITEM2, heuristic='best_width_fit')
        self.sheet.insert(ITEM3, heuristic='best_width_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            correct.insert(ITEM3)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)


class BestHeightFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='best_height_fit')
        self.sheet.insert(ITEM2, heuristic='best_width_fit')
        self.sheet.insert(ITEM3, heuristic='best_width_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            correct.insert(ITEM3)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)


class BestAreaFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='best_height_fit')
        self.sheet.insert(ITEM2, heuristic='best_width_fit')
        self.sheet.insert(ITEM3, heuristic='best_width_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            correct.available_width = 4
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            correct.insert(ITEM3)
            correct.available_width = 1
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)


class WorstWidthFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='worst_width_fit')
        self.sheet.insert(ITEM2, heuristic='worst_width_fit')
        self.sheet.insert(ITEM3, heuristic='worst_width_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            correct.insert(ITEM3)
            correct.available_width = 2
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.insert(ITEM2)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)


class WorstHeightFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 5)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 3)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='worst_height_fit')
        self.sheet.insert(ITEM2, heuristic='worst_height_fit')
        self.sheet.insert(ITEM3, heuristic='worst_height_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.insert(ITEM)
            self.assertEqual(self.sheet.shelves[0].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = shelf.Shelf(8, 3, 2)
            correct.insert(ITEM2)
            correct.insert(ITEM3)
            self.assertEqual(self.sheet.shelves[1].__dict__,
                             correct.__dict__)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 13)


class WorstAreaFit(BaseTestCase):
    def setUp(self):
        self.sheet = shelf.Sheet(8, 4)


    def tearDown(self):
        del self.sheet


    def testThreeInserts(self):
        """
        Three items across two shelves
        """
        ITEM = item.Item(4, 2)
        ITEM2 = item.Item(5, 2)
        ITEM3 = item.Item(2, 2)
        self.sheet.insert(ITEM, heuristic='worst_area_fit')
        self.sheet.insert(ITEM2, heuristic='worst_area_fit')
        self.sheet.insert(ITEM3, heuristic='worst_area_fit')
        with self.subTest():
            correct = shelf.Shelf(8, 2, 0)
            correct.items = [ITEM, ITEM3]
            correct.available_width = 2
            self.assertCountEqual(self.sheet.shelves[0].items, correct.items)
        with self.subTest():
            correct = shelf.Shelf(8, 2, 2)
            correct.items = [ITEM2]
            correct.available_width = 3
            self.assertCountEqual(self.sheet.shelves[1].items, correct.items)
        with self.subTest():
            correct = [ITEM, ITEM2, ITEM3]
            self.assertCountEqual(self.sheet.items, correct)
        with self.subTest():
            self.assertEqual(self.sheet.free_area, 10)


#class BinStats(BaseTestCase):
#    def setUp(self):
#        self.ROOT = bintree.BinTree()
#        self.ROOT.insert(bintree.Item(4, 4))
#        self.ROOT.insert(bintree.Item(2, 2))
#
#    def testReturn(self):
#        expected_result = {'area': 32,
#                           'efficiency': 0.625,
#                           'height': 8,
#                           'items': [(bintree.CornerPoint(x=0, y=0),
#                                        bintree.Item(width=4, height=4)),
#                                     (bintree.CornerPoint(x=0, y=4),
#                                        bintree.Item(width=2, height=2))],
#                           'width': 4
#                          }
#        self.assertEqual(bintree.bin_stats(self.ROOT), expected_result)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(shelfObject))
        suite.addTests(loader.loadTestsFromTestCase(NextFit))
        suite.addTests(loader.loadTestsFromTestCase(NextFitNoRotation))
        suite.addTests(loader.loadTestsFromTestCase(FirstFit))
        suite.addTests(loader.loadTestsFromTestCase(BestWidthFit))
        suite.addTests(loader.loadTestsFromTestCase(BestHeightFit))
        suite.addTests(loader.loadTestsFromTestCase(BestAreaFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstWidthFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstHeightFit))
        suite.addTests(loader.loadTestsFromTestCase(WorstAreaFit))
        suite.addTests(loader.loadTestsFromTestCase(WasteMap))
        #suite.addTests(loader.loadTestsFromTestCase(BinStats))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite

