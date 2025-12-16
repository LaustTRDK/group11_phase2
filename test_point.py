import unittest
import random

from point.py import Point


class Test_point(unittest.TestCase):

    def test_distance_to(self):
        p1 = Point(10, 10)
        p2 = Point(13, 14)
        expected = 5.0
        calcu = p1.distance_to(p2)

        self.assertAlmostEqual(calcu, expected)

    def test_negativ_value_x(self):
        """Confirms taht when a point have a negative value that the specefic exception
        ValueError is raised."""
        with self.assertRaises(ValueError):
            Point(-1, 10)

    def test_negative_value_y(self):
        with self.assertRaises(ValueError):
            Point(10, -1)

    def test_not_inside_grid_x(self):
        with self.assertRaises(ValueError):
            Point(100, 5)
    
    def test_not_insde_grid_y(self):
        with self.assertRaises(ValueError):
            Point(40, 100)

    def test_non_numeric_point_values_x(self):
        with self.assertRaises(ValueError):
            Point("hehe", 5)
    
    def test_non_numeric_point_values_y(self):
        with self.assertRaises(ValueError):
            Point(5, "haha")
    
    def test_get_point(self):
        p = Point(10, 5)
        res = p.get_point()
        
        self.assertEqual(res, (10, 5))

    def test_set_point(self):
        q = Point()
        q.set_point(3, 3)
        self.assertEqual(q.x, 3)
        self.assertEqual(q.y, 3)

    def test_copy_Point(self):
        q = Point()
        q.set_point(3, 3)
        copy = q.copy_point()
        self.assertEqual(copy.x, 3)
        self.assertEqual(copy.y, 3)

    def test_copy_pint_is_new_obect(self):
        q = Point()
        q.set_point(3, 3)
        copy = q.copy_point()
        self.assertIsNot(copy, q)

    def test_add_point_to_point(self):
        p = Point(2, 2)
        q = Point(3, 3)
        r = q + p

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)
        self.assertIsNot(r, p)

    def test_add_number_to_point(self):
        p = Point(2, 2)
        r = p + 3

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)
        self.assertIsNot(r, p)

    def test_add_invalid_value(self):
        p = Point(1, 1)
        with self.assertRaises(ValueError):
            p + "duckling"

    def test_sub_point(self):
        p = Point(2, 2)
        q = Point(5, 5)
        r = q - p

        self.assertEqual(r.x, 3)
        self.assertEqual(r.y, 3)


    def test_sub_number(self):
        p = 2
        q = Point(5, 5)
        r = q - p

        self.assertEqual(r.x, 3)
        self.assertEqual(r.y, 3)

    def test_sub_invalid_value(self):
        p = Point(1, 1)
        with self.assertRaises(ValueError):
            p - "Antonio"

    def test_iadd_point_to_point(self):
        r = Point(2, 2)
        q = Point(3, 3)

        orginal_id = id(r)
        r += q

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)
        self.assertEqual(id(r), orginal_id)

    def test_iadd_point_to_value(self):
        r = Point(2, 2)
        r += 3

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)
        
    def test_isub_point_to_point(self):
        r = Point(8, 8)
        q = Point(3, 3)

        orginal_id = id(r)
        r -= q

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)
        self.assertEqual(id(r), orginal_id)

    def test_isub_point_to_value(self):
        r = Point(8, 8)
        r -= 3

        self.assertEqual(r.x, 5)
        self.assertEqual(r.y, 5)

    def test_mul_point(self):
        p = Point(2, 3)
        q = Point(4, 5)

        r = p * q

        self.assertEqual(r.x, 8)
        self.assertEqual(r.y, 15)

    def test_mul_number(self):
        p = Point(3, 3)
        
        r = p * 2

        self.assertEqual(r.x, 6)
        self.assertEqual(r.y, 6)
        