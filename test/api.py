import sys
import unittest
from io import StringIO

import binpack

from .base import BaseTestCase
from .util import stdout_redirect

class APITests(BaseTestCase):

    def testReadme(self):
        """
        mostly naive test of documented functionality
        """
        BINSET = binpack.BinPack(bin_size=(4,8))
        BINSET.insert(
            (2, 4), (2, 2), (4, 5), (4, 4), (2, 2), (3, 2),
            heuristic='best_fit')
        print_out_io = StringIO()
        with stdout_redirect(print_out_io):
            BINSET.print_stats()
        print_out = print_out_io.read().strip()
        expected_out = '\n'.join([
            "{'width': 4, 'height': 8, 'area': 32, 'efficiency': 0.8125, 'items': [(CornerPoint(x=0, y=0), Item(width=4, height=5)), (CornerPoint(x=0, y=5), Item(width=3, height=2))]}",
            "{'width': 4, 'height': 8, 'area': 32, 'efficiency': 1.0, 'items': [(CornerPoint(x=0, y=0), Item(width=4, height=4)), (CornerPoint(x=0, y=4), Item(width=2, height=4)), (CornerPoint(x=2, y=4), Item(width=2, height=2)), (CornerPoint(x=2, y=6), Item(width=2, height=2))]}",
            ])
        self.assertEqual(
            print_out,
            expected_out
            )


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
