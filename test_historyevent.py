import unittest 

from historyevent import historyevent 


class TestHistoryEventInit(unittest.TestCase):

    def test_valid_event_minimal(self):
        """This to validation creation of a historyevent"""
        ev = historyevent(timestamp=5, event="ASSIGNED")

        self.assertEqual(ev.timestamp, 5)
        self.assertEqual(ev.event, "ASSIGNED")
        self.assertIsNone(ev.request_id)
        self.assertIsNone(ev.earnings)

    def test_valid_event_full(self):
        """This is to validate a full event"""
    ev = historyevent(
        timestamp=10,
        event="DELIVERED",
        request_id=3,
        earnings=120,
        behaviour="greedy"
    )

    self.assertEqual(ev.request_id, 3)
    self.assertEqual(ev.earnings, 120)
    self.assertEqual(ev.behaviour, "greedy")

class TestHistoryEventValidation(unittest.TestCase):
    """This is to validate it when we will expect it to fail"""

    def test_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            historyevent(-1, "ASSIGNED")

    def test_invalid_event_type(self):
        with self.assertRaises(ValueError):
            historyevent(5, 123)

    def test_invalid_request_id(self):
        with self.assertRaises(ValueError):
            historyevent(5, "ASSIGNED", request_id=-2)

    def test_invalid_earnings(self):
        with self.assertRaises(ValueError):
            historyevent(5, "DELIVERED", earnings=-10)
