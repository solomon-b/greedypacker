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
        M = binpack.BinManager(8, 4, algo='shelf')
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


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(APITests))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite
