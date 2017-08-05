import unittest

from . import api as api_tests
from . import test_bintree

def load_tests(loader, standard_tests, pattern):
    if pattern == __name__:
        pattern = None
    suite = unittest.TestSuite()
    for test_module in [
        api_tests,
        test_bintree,
    ]:
        tests = (unittest.defaultTestLoader
                 .loadTestsFromModule(test_module, pattern=pattern))
        suite.addTests(tests)
    return suite
