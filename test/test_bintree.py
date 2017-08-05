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


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(SingleInsertion))
        suite.addTests(loader.loadTestsFromTestCase(TwoInsertion))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite

