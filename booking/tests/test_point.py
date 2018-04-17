import unittest
from taxi_booking.booking.point import Point, manhattan_dist


class TestPoint(unittest.TestCase):

    def test_manhattan_dist_0_translation(self):
        self.assertEqual(0, manhattan_dist(src=Point(0, 0), dst=Point(0, 0)))

    def test_manhattan_dist_positive_and_negative_x_axis_translation(self):
        self.assertEqual(2, manhattan_dist(src=Point(0, 0), dst=Point(2, 0)))
        self.assertEqual(2, manhattan_dist(src=Point(0, 0), dst=Point(-2, 0)))
        self.assertEqual(2, manhattan_dist(src=Point(2, 0), dst=Point(0, 0)))
        self.assertEqual(2, manhattan_dist(src=Point(-2, 0), dst=Point(0, 0)))

    def test_manhattan_dist_positive_and_negative_y_axis_translation(self):
        self.assertEqual(2, manhattan_dist(src=Point(0, 0), dst=Point(0, 2)))
        self.assertEqual(2, manhattan_dist(src=Point(0, 0), dst=Point(0, -2)))
        self.assertEqual(2, manhattan_dist(src=Point(0, 2), dst=Point(0, 0)))
        self.assertEqual(2, manhattan_dist(src=Point(0, -2), dst=Point(0, 0)))

    def test_manhattan_dist_positive_and_negative_x_and_y_axis_translation(self):
        self.assertEqual(6, manhattan_dist(src=Point(1, 1), dst=Point(4, 4)))
        self.assertEqual(6, manhattan_dist(src=Point(4, 4), dst=Point(1, 1)))
        self.assertEqual(6, manhattan_dist(src=Point(-1, -1), dst=Point(-4, -4)))
        self.assertEqual(6, manhattan_dist(src=Point(-4, -4), dst=Point(-1, -1)))

    def test_manhattan_dist_reflection_about_line_y_equal_x(self):
        self.assertEqual(10, manhattan_dist(src=Point(-1, 1), dst=Point(4, -4)))
        self.assertEqual(10, manhattan_dist(src=Point(1, -1), dst=Point(-4, 4)))

    def test_manhattan_dist_32_bit_integers(self):
        min_int = -2147483648
        max_int = 2147483647
        self.assertEqual(8589934590, manhattan_dist(src=Point(min_int, min_int),
                                                    dst=Point(max_int, max_int)))


if __name__ == '__main__':
    unittest.main()
