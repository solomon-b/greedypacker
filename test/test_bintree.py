import sys
import unittest

from binpack import bintree

from .base import BaseTestCase
from .util import stdout_redirect

class SingleInsertion(BaseTestCase):
    def setUp(self):
        self.ROOT = bintree.BinTree()
        self.ROOT.insert(bintree.Item(4, 4))

    def testOccupied(self):
        self.assertEqual(self.ROOT.occupied, bintree.Item(4, 4))

    def testLargestChild(self):
        self.assertEqual(self.ROOT.largest_child, (4, 4))

    def testDims(self):
        self.assertEqual((self.ROOT.width, self.ROOT.height), (4, 4))

    def testRight(self):
        self.assertIsNone(self.ROOT.right)

    def testBottom(self):
        self.assertIsNotNone(self.ROOT.bottom)


class TwoInsertion(BaseTestCase):
    def setUp(self):
        self.ROOT = bintree.BinTree()
        self.ROOT.insert(bintree.Item(4, 4))
        self.ROOT.insert(bintree.Item(2, 2))
        self.CHILD = self.ROOT.bottom

    def testOccupied(self):
        self.assertEqual(self.CHILD.occupied, bintree.Item(2, 2))

    def testLargestChild(self):
        self.assertEqual(self.ROOT.largest_child, (4, 2))

    def testDims(self):
        self.assertEqual((self.CHILD.width, self.CHILD.height), (2, 2))

    def testChildren(self):
        self.assertIsNotNone(self.CHILD.right)
        self.assertIsNotNone(self.CHILD.bottom)

    def testChildRightDims(self):
        self.assertEqual((self.CHILD.right.width, self.CHILD.right.height), (2, 2))

    def testChildBottomDims(self):
        self.assertEqual((self.CHILD.bottom.width, self.CHILD.bottom.height), (4, 2))


class BinStats(BaseTestCase):
    def setUp(self):
        self.ROOT = bintree.BinTree()
        self.ROOT.insert(bintree.Item(4, 4))
        self.ROOT.insert(bintree.Item(2, 2))

    def testReturn(self):
        expected_result = {'area': 32,
                           'efficiency': 0.625,
                           'height': 8,
                           'items': [(bintree.CornerPoint(x=0, y=0),
                                        bintree.Item(width=4, height=4)),
                                     (bintree.CornerPoint(x=0, y=4),
                                        bintree.Item(width=2, height=2))],
                           'width': 4
                          }
        self.assertEqual(bintree.bin_stats(self.ROOT), expected_result)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(SingleInsertion))
        suite.addTests(loader.loadTestsFromTestCase(TwoInsertion))
        suite.addTests(loader.loadTestsFromTestCase(BinStats))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite

