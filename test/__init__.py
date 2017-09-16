import unittest

from . import test_api
from . import test_bintree
from . import test_shelf
#from . import test_guillotine
from . import test_binpack

def load_tests(loader, standard_tests, pattern):
    if pattern == __name__:
        pattern = None
    suite = unittest.TestSuite()
    for test_module in [
        #test_api,
        #test_bintree,
        test_shelf,
        #test_guillotine,
        #test_binpack,
    ]:
        tests = (unittest.defaultTestLoader
                 .loadTestsFromModule(test_module, pattern=pattern))
        suite.addTests(tests)
    return suite
