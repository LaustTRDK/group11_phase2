import unittest

from point import Point
from request import Request
from offer import Offer
from driver import driver
from driverbehaviour import (
    GreedyDistanceBehaviour,
    EarningsMaxBehaviour,
    LazyBehaviour,
    Naive
)

def make_driver(position, speed=1.0, idle_time=0, behaviour=None):
    d = driver(
        did=1,
        position=position,
        speed=speed,
        status="IDLE",
        current_request=None,
        behaviour=behaviour
    )
    d.idle_time = idle_time
    return d

class TestGreedyDistanceBehaviour(unittest.TestCase):
    """Testting greedy behavior"""

    def test_accepts_close_pickup(self):
        behaviour = GreedyDistanceBehaviour(expiretime=20)
        d = make_driver(Point(0, 0), speed=1, behaviour=behaviour)

        req = Request(
            rid=1,
            pickup=Point(2, 0),
            dropoff=Point(4, 0),
            created=0
        )
        offer = Offer(req)

        self.assertTrue(behaviour.decide(d, offer, time=0))

    def test_rejects_far_pickup(self):
        behaviour = GreedyDistanceBehaviour(expiretime=20)
        d = make_driver(Point(0, 0), speed=1, behaviour=behaviour)

        req = Request(
            rid=2,
            pickup=Point(50, 0),
            dropoff=Point(55, 0),
            created=0
        )
        offer = Offer(req)

        self.assertFalse(behaviour.decide(d, offer, time=0))

class TestEarningsMaxBehaviour(unittest.TestCase):
    """Testting earning behavior"""

    def test_accepts_good_ratio(self):
        behaviour = EarningsMaxBehaviour(min_ratio=0.3)
        d = make_driver(Point(0, 0), speed=2, behaviour=behaviour)

        req = Request(
            rid=1,
            pickup=Point(1, 0),
            dropoff=Point(6, 0),
            created=0
        )
        offer = Offer(req)

        self.assertTrue(behaviour.decide(d, offer, time=0))

    def test_rejects_bad_ratio(self):
        behaviour = EarningsMaxBehaviour(min_ratio=1.0)
        d = make_driver(Point(0, 0), speed=1, behaviour=behaviour)

        req = Request(
            rid=2,
            pickup=Point(10, 0),
            dropoff=Point(20, 0),
            created=0
        )
        offer = Offer(req)

        self.assertFalse(behaviour.decide(d, offer, time=0))

class TestLazyBehaviour(unittest.TestCase):
    """Testting the lasy behavior"""

    def test_accepts_when_idle_long_enough(self):
        behaviour = LazyBehaviour(close=5, max_idle_time=6)
        d = make_driver(
            Point(0, 0),
            speed=1,
            idle_time=10,
            behaviour=behaviour
        )

        req = Request(
            rid=1,
            pickup=Point(3, 0),
            dropoff=Point(6, 0),
            created=0
        )
        offer = Offer(req)

        self.assertTrue(behaviour.decide(d, offer, time=10))

    def test_rejects_when_not_idle_long_enough(self):
        behaviour = LazyBehaviour(close=5, max_idle_time=6)
        d = make_driver(
            Point(0, 0),
            speed=1,
            idle_time=2,
            behaviour=behaviour
        )

        req = Request(
            rid=2,
            pickup=Point(3, 0),
            dropoff=Point(6, 0),
            created=0
        )
        offer = Offer(req)

        self.assertFalse(behaviour.decide(d, offer, time=2))

class TestNaiveBehaviour(unittest.TestCase):
    """Testing the naive behavior"""

    def test_always_accepts(self):
        behaviour = Naive()
        d = make_driver(Point(0, 0), speed=1, behaviour=behaviour)

        req = Request(
            rid=1,
            pickup=Point(100, 100),
            dropoff=Point(200, 200),
            created=0
        )
        offer = Offer(req)

        self.assertTrue(behaviour.decide(d, offer, time=0))
