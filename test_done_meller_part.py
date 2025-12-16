import unittest
import random

from done_meller_part import Point, request, historyevent, driver, driverbehaviour, greedydistancebehaviour, earningsmaxbehaviour, lazybehaviour, naive, mutationsthresholds, mutationrule, desisionthreerule, requestgenerator, drivergenerator

class Test_point(unittest.TestCase):

    def test_distance_to(self):
        p1 = Point(10, 10)
        p2 = Point(13, 14)
        expected = 5.0
        calcu = p1.distance_to(p2)

        self.assertAlmostEqual(calcu, 5.0)

if __name__ == '__main__':
    unittest.main()