import unittest
import random

from point import Point
from driver import driver
from historyevent import historyevent
from mutation_rule import (
    MutationThresholds,
    DecisionTreeRule
)
from driver_behaviour import (
    GreedyDistanceBehaviour,
    EarningsMaxBehaviour,
    LazyBehaviour,
    Naive
)

def make_driver(behaviour):
    d = driver(
        did=1,
        position=Point(0, 0),
        speed=1.0,
        status="IDLE",
        current_request=None,
        behaviour=behaviour
    )
    d.behaviour_mutation_stamp = 0
    return d

class TestDecisionTreeRule(unittest.TestCase):

    def setUp(self):
        self.thresholds = MutationThresholds(lasttime_mutation_thr=10)
        self.rule = DecisionTreeRule(self.thresholds)

    def test_mutates_when_time_threshold_exceeded(self):
        """Test id the threshold for how long since last mutaton triggers."""
        d = make_driver(GreedyDistanceBehaviour())

        random.seed(0)  # deterministic
        self.rule.maybe_mutate(d, time=10)

        self.assertNotEqual(type(d.behaviour), GreedyDistanceBehaviour)
        self.assertEqual(d.behaviour_mutation_stamp, 10)


    def test_no_mutation_when_thresholds_not_hit(self):
        """Test for when no parameters was triggered"""
        d = make_driver(GreedyDistanceBehaviour())

        # add good history
        d.history.append(historyevent(1, "DELIVERED", earnings=10))
        d.history.append(historyevent(2, "accepted"))

        self.rule.maybe_mutate(d, time=5)

        self.assertIsInstance(d.behaviour, GreedyDistanceBehaviour)
        self.assertEqual(d.behaviour_mutation_stamp, 0)

    def test_expired_threshold_triggers_mutation(self):
        """Test when the expire request threshold is triggered -> A"""
    d = make_driver(Naive())

    # expired events
    for i in range(3):
        d.history.append(historyevent(i, "expired"))

    self.rule.maybe_mutate(d, time=10)

    self.assertIsInstance(d.behaviour, GreedyDistanceBehaviour)
    self.assertEqual(d.behaviour_mutation_stamp, 10)


    def test_low_earnings_triggers_earnings_behaviour(self):
        """Test when low esrnings trigger is triggered -> B"""
        d = make_driver(Naive())

        d.history.append(historyevent(1, "DELIVERED", earnings=1))

        self.rule.maybe_mutate(d, time=10)

        self.assertIsInstance(d.behaviour, EarningsMaxBehaviour)

    def test_low_accepted_triggers_naive(self):
        """Testting when to accepting of request is triggered -> C"""
        d = make_driver(GreedyDistanceBehaviour())

        # no accepted events
        d.history.append(historyevent(1, "DELIVERED", earnings=10))

        self.rule.maybe_mutate(d, time=10)

        self.assertIsInstance(d.behaviour, Naive)

    def test_expired_and_low_earnings(self):
        """Test when trigger A + B """
        d = make_driver(GreedyDistanceBehaviour())

        for i in range(3):
            d.history.append(historyevent(i, "expired"))
        d.history.append(historyevent(1, "DELIVERED", earnings=1))

        random.seed(1)
        self.rule.maybe_mutate(d, time=10)

        self.assertNotEqual(type(d.behaviour), GreedyDistanceBehaviour)
