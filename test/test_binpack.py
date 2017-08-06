import sys
import unittest

import binpack

from .base import BaseTestCase
from .util import stdout_redirect

class PackInstantiation(BaseTestCase):
    def setUp(self):
        self.PACK = binpack.BinPack(bin_size = (4, 8))

    def testBinCount(self):
        self.assertEqual(self.PACK.bin_count, 1)

    def testBinDict(self):
        self.assertEqual(self.PACK.bin_dict['oversized'], [])
        self.assertIsInstance(self.PACK.bin_dict[0], binpack.bintree.BinTree)

    def testBinSize(self):
        self.assertEqual(self.PACK.bin_size, (4, 8))

    def testSorting(self):
        self.assertTrue(self.PACK.sorting)

    def testAVLInstance(self):
        self.assertIsInstance(self.PACK.tree, binpack.avl_tree.AvlTree)


class BestFit(BaseTestCase):
    def setUp(self):
        self.PACK = binpack.BinPack(bin_size = (4, 8))

    def testSingleInsert(self):
        self.PACK.insert((3, 4), heuristic="best_fit")

        expected_result = {0:
                            {'area': 32,
                             'efficiency': 0.375,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                        binpack.bintree.Item(width=3, height=4))],
                             'width': 4},
                           'oversized': []}
        self.assertEqual(self.PACK.print_stats(), expected_result)

    def testMultiInsert(self):
        self.PACK.insert((4, 4), (2, 4), (2, 2), (4, 5), (10, 5), heuristic="best_fit")

        expected_result = {0:
                            {'area': 32,
                             'efficiency': 0.625,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                       binpack.bintree.Item(width=4, height=5))],
                             'width': 4},
                           1:
                            {'area': 32,
                             'efficiency': 0.875,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                       binpack.bintree.Item(width=4, height=4)),
                                       (binpack.bintree.CornerPoint(x=0, y=4),
                                       binpack.bintree.Item(width=2, height=4)),
                                       (binpack.bintree.CornerPoint(x=2, y=4),
                                       binpack.bintree.Item(width=2, height=2))],
                              'width': 4},
                           'oversized': [binpack.bintree.Item(width=10, height=5)]}

        self.assertEqual(self.PACK.print_stats(), expected_result)


class NextFit(BaseTestCase):
    def setUp(self):
        self.PACK = binpack.BinPack(bin_size = (4, 8))

    def testSingleInsert(self):
        self.PACK.insert((3, 4), heuristic="next_fit")

        expected_result = {0:
                            {'area': 32,
                             'efficiency': 0.375,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                        binpack.bintree.Item(width=3, height=4))],
                             'width': 4},
                           'oversized': []}
        self.assertEqual(self.PACK.print_stats(), expected_result)

    def testMultiInsert(self):
        self.PACK.insert((4, 4), (2, 4), (2, 2), (4, 5), (10, 5), heuristic="next_fit")

        expected_result = {0:
                            {'area': 32,
                             'efficiency': 0.75,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                       binpack.bintree.Item(width=4, height=5)),
                                       (binpack.bintree.CornerPoint(x=0, y=5),
                                       binpack.bintree.Item(width=2, height=2))],
                             'width': 4},
                           1:
                            {'area': 32,
                             'efficiency': 0.75,
                             'height': 8,
                             'items': [(binpack.bintree.CornerPoint(x=0, y=0),
                                       binpack.bintree.Item(width=4, height=4)),
                                       (binpack.bintree.CornerPoint(x=0, y=4),
                                       binpack.bintree.Item(width=2, height=4))],
                              'width': 4},
                           'oversized': [binpack.bintree.Item(width=10, height=5)]}

        self.assertEqual(self.PACK.print_stats(), expected_result)


class PrintStats(BaseTestCase):
    def setUp(self):
        self.PACK = binpack.BinPack(bin_size = (4, 8))

    def testPrintStats(self):
        """ empty bintree printout """
        expected_result = {0: {'area': 32,
                               'efficiency': 0.0,
                               'height': 8,
                               'items': [],
                               'width': 4},
                           'oversized': []}
        self.assertEqual(self.PACK.print_stats(), expected_result)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(PackInstantiation))
        suite.addTests(loader.loadTestsFromTestCase(BestFit))
        suite.addTests(loader.loadTestsFromTestCase(NextFit))
        suite.addTests(loader.loadTestsFromTestCase(PrintStats))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite


