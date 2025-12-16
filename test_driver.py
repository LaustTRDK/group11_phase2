import unittest 

from driver import driver 
from point import Point 
from request import request 


class TestDriverInit(unittest.TestCase):
    """This is to validate the construction of a driver"""

    def setUp(self):
        self.pos = Point()
        self.pos.set_point(0, 0)

    def test_valid_driver(self):
        d = driver(
            did=1,
            position=self.pos,
            speed=1.5,
            status="IDLE",
            current_request=None,
            behaviour=None
        )

        self.assertEqual(d.did, 1)
        self.assertEqual(d.status, "IDLE")
        self.assertEqual(d.history, [])

class TestDriverValidation(unittest.TestCase):

    def setUp(self):
        self.pos = Point()
        self.pos.set_point(0, 0)

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            driver(-1, self.pos, 1, "IDLE", None, None)

    def test_invalid_position(self):
        with self.assertRaises(ValueError):
            driver(1, "not_a_point", 1, "IDLE", None, None)

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            driver(1, self.pos, 1, "FLYING", None, None)

class TestDriverValidation(unittest.TestCase):
    """This is to validate that what should fail will"""

    def setUp(self):
        self.pos = Point()
        self.pos.set_point(0, 0)

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            driver(-1, self.pos, 1, "IDLE", None, None)

    def test_invalid_position(self):
        with self.assertRaises(ValueError):
            driver(1, "not_a_point", 1, "IDLE", None, None)

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            driver(1, self.pos, 1, "FLYING", None, None)

class TestDriverHistory(unittest.TestCase):
    """To test the logging of a history to the driver"""

    def setUp(self):
        pos = Point()
        pos.set_point(0, 0)

        self.driver = driver(
            did=1,
            position=pos,
            speed=1,
            status="IDLE",
            current_request=None,
            behaviour="greedy"
        )

    def test_log_event(self):
        self.driver.log_event(5, "ASSIGNED", request_id=2)

        self.assertEqual(len(self.driver.history), 1)
        ev = self.driver.history[0]

        self.assertEqual(ev.timestamp, 5)
        self.assertEqual(ev.event, "ASSIGNED")

class TestDriverBehaviourMutation(unittest.TestCase):
    """Testing some of the methods that are implemented for the behavior part"""

    def setUp(self):
        pos = Point()
        pos.set_point(0, 0)

        self.driver = driver(
            did=1,
            position=pos,
            speed=1,
            status="IDLE",
            current_request=None,
            behaviour="greedy"
        )

    def test_update_behaviour_and_stamp(self):
        self.driver.update_behaviour_and_stamp(10, "lazy")

        self.assertEqual(self.driver.behaviour, "lazy")
        self.assertEqual(self.driver.behaviour_mutation_stamp, 10)


class TestDriverMovement(unittest.TestCase):
    """Testing the driver movement"""

    def setUp(self):
        pos = Point()
        pos.set_point(0, 0)

        pickup = Point()
        pickup.set_point(3, 4)

        req = request(1, pickup, pickup)

        self.driver = driver(
            did=1,
            position=pos,
            speed=5,
            status="TO_PICKUP",
            current_request=req,
            behaviour=None
        )

    def test_step_reaches_target(self):
        self.driver.step(1)

        self.assertAlmostEqual(self.driver.position.x, 3)
        self.assertAlmostEqual(self.driver.position.y, 4)
