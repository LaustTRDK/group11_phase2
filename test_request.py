import unittest
import random

from request impoort request


class RequestTestBase(unittest.TestCase):

    def setUp(self):
        self.pickup = Point()
        self.pickup.set_point(0, 0)

        self.dropoff = Point()
        self.dropoff.set_point(20, 10)

        self.req = request(
            rid=1,
            pickup=self.pickup,
            dropoff=self.dropoff,
            creation_time=0,
            status="WAITING",
            assigned_driver_id=0,
            wait_time=0,
            pickup_wait_time=0,
            delivered_wait_time=0,
            expired_wait_time=0
        )

class TestrequestInit(RequestTestBase):

    def test_valid_request_created(self):
        self.assertEqual(self.req.rid, 1)
        self.assertEqual(self.req.status, "WAITING")

    def test_invalid_rid_raises(self):
        with self.assertRaises(ValueError):
            request(
                rid = -1,
                pickup = self.pickup,
                dropoff = self.dropoff
            )

    def test_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            request(
                rid = 1,
                pickup = self.pickup,
                dropoff = self.dropoff,
                status = "naughty_cat"
            )

class TestRequestIsActive(RequestTestBase):
    """Testing the is_active method working"""

    def test_active_states(self):
        for status in ("WAITING", "ASSIGNED", "PICKED"):
            self.req.status = status
            self.assertTrue(self.req.is_active())

    def test_inactive_states(self):
        for status in ("DELIVERED", "EXPIRED"):
            self.req.status = status
            self.assertFalse(self.req.is_active())

class TestRequestAssignment(RequestTestBase):
    """Testting the assigning and status changing"""

    def test_mark_assigned(self):
        self.req.mark_assigned(3)

        self.assertEqual(self.req.status, "ASSIGNED")
        self.assertEqual(self.req.assigned_driver_id, 3)

class TestRequestPicked(RequestTestBase):
    """Testing the method of marked_picked that changes the status of the
    request to picked and also set what the pickup_wait_time"""

    def test_mark_picked_sets_pickup_wait_time(self):
        self.req.mark_picked(5)

        self.assertEqual(self.req.status, "PICKED")
        self.assertEqual(self.req.pickup_wait_time, 5)

class TestRequestDelivered(RequestTestBase):
    """Testing the method that changes the request status to "PICKED" and 
    also change the set the delivered_wait_time"""

    def test_mark_delivered(self):
        self.req.mark_picked(3)
        self.req.mark_delivered(10)

        self.assertEqual(self.req.status, "DELIVERED")
        self.assertEqual(self.req.delivered_wait_time, 7)

class TestRequestExpired(RequestTestBase):
    """Test the method to marked the request as expired"""

    def test_mark_expired(self):
        self.req.mark_expired(8)

        self.assertEqual(self.req.status, "EXPIRED")
        self.assertEqual(self.req.expired_wait_time, 8)

class TestRequestWaitTime(RequestTestBase):
    """Test the metod that can update the wait time"""

    def test_update_wait_time(self):
        self.req.update_wait(12)
        self.assertEqual(self.req.wait_time, 12)

class TestRequestGetters(RequestTestBase):
    """Testing not all the getters methods but only some of them, they are 
    build somewhat the same so testing a few will show that generally the 
    getters methods works"""

    def test_get_rid(self):
        self.assertEqual(self.req.get_request_rid(), 1)

    def test_get_pickup(self):
        """The assertIs(a, b) is a method can vertify if a identical to b,
        akin to the expression a is b"""
        self.assertIs(self.req.get_request_pickup(), self.pickup)

class TestRequestSetters(RequestTestBase):
    """Testing not all the setters methods but only some of them, they are
    build somewhat the same so testing a frw will show that generally the 
    setters methods works"""

    def test_set_status(self):
        self.req.set_request_status("DELIVERED")
        self.assertEqual(self.req.status, "DELIVERED")

    def test_set_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            self.req.set_request_status("Alien_pet")
