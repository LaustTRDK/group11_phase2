import unittest
import random
import numpy as np

from point import Point
from request import Request
from request_generator import RequestGenerator

class TestRequestGenerator(unittest.TestCase):

    def test_init_sets_attributes(self):
        """test constructor"""
        rg = RequestGenerator(rate=2.5, width=100, height=50)

        self.assertEqual(rg.rate, 2.5)
        self.assertEqual(rg.width, 100)
        self.assertEqual(rg.height, 50)
        self.assertEqual(rg._next_rid, 1)
        self.assertEqual(rg.scheduled, [])

    def test_maybe_generate_returns_scheduled_requests(self):
        """Test the generate reques"""
        r1 = Request(1, Point(1, 1), Point(2, 2), creation_time=5)
        r2 = Request(2, Point(3, 3), Point(4, 4), creation_time=5)

        rg = RequestGenerator(rate=0, scheduled=[r1, r2])

        result = rg.maybe_generate(time=5)

        self.assertEqual(result, [r1, r2])
        self.assertEqual(rg.scheduled, [])

    def test_request_ids_increment(self):
        """Test if request id increases correctly"""
        random.seed(1)
        np.random.seed(1)

        rg = RequestGenerator(rate=1)

        reqs1 = rg.req_generate(time=0, req_rate=1)
        reqs2 = rg.req_generate(time=1, req_rate=1)

        all_ids = [r.rid for r in reqs1 + reqs2]

        self.assertEqual(all_ids, sorted(all_ids))
        self.assertEqual(len(set(all_ids)), len(all_ids))

    def test_generated_points_within_bounds(self):
        """Thest that the generated point is inside the grid bounds"""
        random.seed(2)
        np.random.seed(2)

        rg = RequestGenerator(rate=5, width=50, height=30)
        requests = rg.req_generate(time=0, req_rate=5)

        for r in requests:
            self.assertTrue(0 <= r.pickup.x <= 50)
            self.assertTrue(0 <= r.pickup.y <= 30)
            self.assertTrue(0 <= r.dropoff.x <= 50)
            self.assertTrue(0 <= r.dropoff.y <= 30)

import unittest
from driver_generator import DriverGenerator

class TestDriverGenerator(unittest.TestCase):
    """Testing the driver generator"""

    def test_generate_creates_valid_drivers(self):
        dg = DriverGenerator()
        drivers = dg.generate(5)
        self.assertEqual(len(drivers), 5)
        self.assertTrue(all(0 <= d.position.x <= 50 and 0 <= d.position.y <= 30 and 0.5 <= d.speed <= 3.0 for d in drivers))
