import sys
import unittest

from greedypacker import skyline
from greedypacker import item
from greedypacker import guillotine
from .base import BaseTestCase
from .util import stdout_redirect


class Methods(BaseTestCase):
    def setUp(self):
        self.S = skyline.Skyline(8, 4)


    def tearDown(self):
        del self.S


    def testClipSegmentFullOverlap(self):
        """
        Segmented fully adjacent to item
        """
        I = item.Item(4, 1, CornerPoint=[0,0])
        S = skyline.SkylineSegment(0, 0, 4) 
        res = self.S.clip_segment(S, I)

        self.assertEqual(res, [])


    def testClipSegmentExtendsLeft(self):
        """
        Segmented hangs over left
        """
        I = item.Item(4, 1, CornerPoint=[2,0])
        S = skyline.SkylineSegment(0, 0, 4) 
        res = self.S.clip_segment(S, I)

        self.assertEqual(res, [skyline.SkylineSegment(0,0,2)])


    def testClipSegmentExtendsRight(self):
        """
        Segmented hangs over left
        """
        I = item.Item(4, 1, CornerPoint=[0,0])
        S = skyline.SkylineSegment(2, 0, 4) 
        res = self.S.clip_segment(S, I)

        self.assertEqual(res, [skyline.SkylineSegment(4,0,2)])


    def testClipSegmentExtendsBoth(self):
        """
        Segmented hangs over left
        """
        I = item.Item(2, 1, CornerPoint=[2,0])
        S = skyline.SkylineSegment(0, 0, 6) 
        res = self.S.clip_segment(S, I)

        self.assertCountEqual(res, [skyline.SkylineSegment(0, 0, 2), skyline.SkylineSegment(4,0,2)])


    def testUpdateSegment(self):
        """
        Clip initial (0,0,8) segment
        with a (2,2) item at (0,0)
        """
        I = item.Item(2, 2, CornerPoint=[0,0])
        S1 = skyline.SkylineSegment(0, 2, 2)
        S2 = skyline.SkylineSegment(2, 0, 6)

        res = self.S.update_segment(self.S.skyline[0], 0, I)
        self.assertCountEqual(res, [S1, S2])

    
    def testMergeSegments(self):
        """
        Two segment merge
        """
        S1 = skyline.SkylineSegment(0, 0, 2)
        S2 = skyline.SkylineSegment(2, 0, 6)
        S3 = skyline.SkylineSegment(0, 0, 8)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2])
        self.S.merge_segments()
        self.assertEqual(self.S.skyline, [S3])


    def testMergeThreeSegments(self):
        """
        Three segment merge
        """
        S1 = skyline.SkylineSegment(0, 0, 2)
        S2 = skyline.SkylineSegment(2, 0, 4)
        S3 = skyline.SkylineSegment(6, 0, 2)
        S4 = skyline.SkylineSegment(0, 0, 8)
        self.S.skyline.pop()
        self.S.skyline.update([S1, S2, S3])
        self.S.merge_segments()
        self.assertEqual(self.S.skyline, [S4])
        

    def testCheckFitTrue(self):
        """
        Assert item does fit above line segment
        """
        I = item.Item(2, 2, CornerPoint=[0,0])
        S1 = skyline.SkylineSegment(0, 1, 2)
        S2 = skyline.SkylineSegment(2, 0, 6)
        self.S.skyline.pop()
        self.S.skyline.extend([S1, S2])
        self.assertEqual(self.S.check_fit(I.width, I.height, 0), (True, 1))


    def testCheckFitFalse(self):
        """
        Assert item does fit above line segment
        """
        I = item.Item(2, 2, CornerPoint=[0,0])
        S1 = skyline.SkylineSegment(0, 0, 1)
        S2 = skyline.SkylineSegment(1, 3, 7)
        self.S.skyline.pop()
        self.S.skyline.extend([S1, S2])
        self.assertEqual(self.S.check_fit(I.width, I.height, 1), (False, None))

    
    def testCalcWaste(self):
        """
        2 wasted space after insertion
        """
        I0 = item.Item(2, 2)
        I1 = item.Item(2, 1)
        I2 = item.Item(3, 3)
        I3 = item.Item(3, 2)
        I4 = item.Item(4, 2)

        self.S.insert(I0, 'bottom_left')
        self.S.insert(I1, 'bottom_left')
        self.S.insert(I2, 'bottom_left')
        self.S.insert(I3, 'bottom_left')

        wasted_area = self.S.calc_waste(0, I4, 3)
        self.assertEqual(wasted_area, 2)


    def testCalcWaste2(self):
        """
        No wasted Space after insertion
        """
        I0 = item.Item(2, 2)
        I1 = item.Item(2, 1)
        I2 = item.Item(3, 3)
        I3 = item.Item(2, 2)

        self.S.insert(I0, 'bottom_left')
        self.S.insert(I1, 'bottom_left')
        self.S.insert(I2, 'bottom_left')

        wasted_area = self.S.calc_waste(0, I3, 2)
        self.assertEqual(wasted_area, 0)


class BottomLeft(BaseTestCase):
    def setUp(self):
        self.S = skyline.Skyline(8, 5)


    def tearDown(self):
        del self.S

    
    def testOneItemInsert(self):
        """
        Single Item Fits
        """
        I = item.Item(2, 2)
        self.S.insert(I, 'bottom_left')
        S1 = skyline.SkylineSegment(0, 2, 2)
        S2 = skyline.SkylineSegment(2, 0, 6)
        self.assertCountEqual(self.S.skyline, [S1, S2])


    def testMultiItemInsert(self):
        """
        5 item insertion to match Figure 7 from
        Jukka's article.
        """
        I0 = item.Item(2, 2)
        I1 = item.Item(2, 1)
        I2 = item.Item(3, 3)
        I3 = item.Item(3, 2)
        I4 = item.Item(4, 2)
        self.S.insert(I0, 'bottom_left')
        self.S.insert(I1, 'bottom_left')
        self.S.insert(I2, 'bottom_left')
        self.S.insert(I3, 'bottom_left')
        self.S.insert(I4, 'bottom_left')
        S0 = skyline.SkylineSegment(0, 4, 3)
        S1 = skyline.SkylineSegment(7, 0, 1)
        with self.subTest():
            self.assertCountEqual(self.S.skyline, [S1, S0])
        with self.subTest():
            self.assertEqual(self.S.free_area, 11)


class BestFit(BaseTestCase):
    def setUp(self):
        self.S = skyline.Skyline(8, 5)


    def tearDown(self):
        del self.S

    
    def testOneItemInsert(self):
        """
        Single Item Fits
        """
        I = item.Item(2, 2)
        self.S.insert(I, 'best_fit')
        S1 = skyline.SkylineSegment(0, 2, 2)
        S2 = skyline.SkylineSegment(2, 0, 6)
        self.assertCountEqual(self.S.skyline, [S1, S2])


    def testMultiItemInsert(self):
        """
        5 item insertion
        """
        I0 = item.Item(2, 2)
        I1 = item.Item(2, 1)
        I2 = item.Item(3, 3)
        I3 = item.Item(3, 2)
        I4 = item.Item(4, 2)
        self.S.insert(I0, 'best_fit')
        self.S.insert(I1, 'best_fit')
        self.S.insert(I2, 'best_fit')
        self.S.insert(I3, 'best_fit')
        self.S.insert(I4, 'best_fit')

        S0 = skyline.SkylineSegment(0, 2, 3)
        S1 = skyline.SkylineSegment(7, 3, 1)
        with self.subTest():
            self.assertCountEqual(self.S.skyline, [S1, S0])
        with self.subTest():
            self.assertEqual(self.S.free_area, 11)


class WasteMap(BaseTestCase):
    def setUp(self):
        self.S = skyline.Skyline(8, 5)
        I0 = item.Item(2, 2)
        I1 = item.Item(2, 1)
        I2 = item.Item(3, 3)
        I3 = item.Item(3, 2)
        I4 = item.Item(4, 2)
        self.S.insert(I0, 'bottom_left')
        self.S.insert(I1, 'bottom_left')
        self.S.insert(I2, 'bottom_left')
        self.S.insert(I3, 'bottom_left')
        self.S.insert(I4, 'bottom_left')

    def tearDown(self):
        del self.S


    def testWastemapCreation(self):
        """
        5 item insertion to match Figure 7 from
        Jukka's article.
        """
        F0 = guillotine.FreeRectangle(1, 1, 2, 1)
        F1 = guillotine.FreeRectangle(1, 2, 3, 1)

        self.assertCountEqual(self.S.wastemap.freerects, [F0, F1])
        

    def testWastemapInsertion(self):
        """
        5 item insertion to match Figure 7 from
        Jukka's article.
        """
        I5 = item.Item(1, 2)
        self.S.insert(I5)
        self.assertEqual(I5.x, 3)
        self.assertEqual(I5.y, 1)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    if pattern is None:
        suite.addTests(loader.loadTestsFromTestCase(Methods))
        suite.addTests(loader.loadTestsFromTestCase(BottomLeft))
        suite.addTests(loader.loadTestsFromTestCase(BestFit))
        suite.addTests(loader.loadTestsFromTestCase(WasteMap))
    else:
        tests = loader.loadTestsFromName(pattern,
                                         module=sys.modules[__name__])
        failedTests = [t for t in tests._tests
                       if type(t) == unittest.loader._FailedTest]
        if len(failedTests) == 0:
            suite.addTests(tests)
    return suite

