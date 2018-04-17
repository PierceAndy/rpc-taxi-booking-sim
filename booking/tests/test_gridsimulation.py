import unittest
from taxi_booking.booking.gridsimulation import GridSimulation
from taxi_booking.booking.point import Point
from taxi_booking.booking.trip import Trip


class TestGridSimulation(unittest.TestCase):

    def setUp(self):
        start_location = Point(0, 0)
        num_taxis = 3
        self.simulation = GridSimulation(start_location, num_taxis)
        self.trip = Trip({'source': {'x': 1, 'y': 1},
                          'destination': {'x': 4, 'y': 4}})

    def test_book_for_1_booking(self):
        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))

    def test_book_for_taxi_at_pickup_location(self):
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 4, 'y': 4}})
        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(trip))

    def test_book_for_booking_src_equal_dst(self):
        trip = Trip({'source': {'x': 1, 'y': 1},
                     'destination': {'x': 1, 'y': 1}})
        self.assertIsNone(self.simulation.book(trip))

        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))

    def test_book_for_3_consecutive_bookings(self):
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 2}})
        expected_response = {'car_id': 1, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))

        trip = Trip({'source': {'x': 1, 'y': 1},
                     'destination': {'x': 4, 'y': 4}})
        expected_response = {'car_id': 2, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(trip))

        trip = Trip({'source': {'x': -1, 'y': -1},
                     'destination': {'x': 4, 'y': 4}})
        expected_response = {'car_id': 3, 'total_time': 12}
        self.assertEqual(expected_response, self.simulation.book(trip))

    def test_book_for_no_free_taxis(self):
        self.simulation.book(self.trip)
        self.simulation.book(self.trip)
        self.simulation.book(self.trip)
        self.assertIsNone(self.simulation.book(self.trip))

    def test_book_for_32_bit_int(self):
        # Edge case for 32-bit integers
        min_int = -2147483648
        max_int = 2147483647

        start_location = Point(min_int, min_int)
        num_taxis = 1
        self.simulation = GridSimulation(start_location, num_taxis)

        trip = Trip({'source': {'x': max_int, 'y': max_int},
                     'destination': {'x': min_int, 'y': min_int}})
        expected_response = {'car_id': 1, 'total_time': 17179869180}
        self.assertEqual(expected_response, self.simulation.book(trip))

    def test_reset_for_1_booking(self):
        self.simulation.book(self.trip)
        self.simulation.reset()
        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))

    def test_reset_for_3_consecutive_bookings(self):
        self.simulation.book(self.trip)
        self.simulation.book(self.trip)
        self.simulation.book(self.trip)
        self.simulation.reset()
        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))

    def test_increment_time_consecutively_for_0_bookings(self):
        self.simulation.increment_time()
        self.simulation.increment_time()
        self.simulation.increment_time()

    def test_increment_time_for_1_complete_booking(self):
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 2}})
        expected_response = {'car_id': 1, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))

        self.simulation.increment_time()
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 2}})
        expected_response = {'car_id': 2, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))

        self.simulation.increment_time()
        trip = Trip({'source': {'x': 0, 'y': 2},
                     'destination': {'x': 0, 'y': 0}})
        expected_response = {'car_id': 1, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))

    def test_increment_time_for_3_simultaneous_identical_bookings(self):
        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))
        expected_response = {'car_id': 2, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))
        expected_response = {'car_id': 3, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(self.trip))

        for i in range(8):
            self.assertIsNone(self.simulation.book(self.trip))
            self.simulation.increment_time()

        trip = Trip({'source': {'x': 1, 'y': 1},
                     'destination': {'x': 0, 'y': 0}})

        expected_response = {'car_id': 1, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(trip))
        expected_response = {'car_id': 2, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(trip))
        expected_response = {'car_id': 3, 'total_time': 8}
        self.assertEqual(expected_response, self.simulation.book(trip))

    def test_increment_time_for_3_simultaneous_bookings(self):
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 2}})
        expected_response = {'car_id': 1, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 3}})
        expected_response = {'car_id': 2, 'total_time': 3}
        self.assertEqual(expected_response, self.simulation.book(trip))

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 4}})
        expected_response = {'car_id': 3, 'total_time': 4}
        self.assertEqual(expected_response, self.simulation.book(trip))

        for i in range(2):
            self.assertIsNone(self.simulation.book(self.trip))
            self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 10, 'y': 10}})
        expected_response = {'car_id': 1, 'total_time': 22}
        self.assertEqual(expected_response, self.simulation.book(trip))

        self.simulation.increment_time()
        expected_response = {'car_id': 2, 'total_time': 23}
        self.assertEqual(expected_response, self.simulation.book(trip))

        self.simulation.increment_time()
        expected_response = {'car_id': 3, 'total_time': 24}
        self.assertEqual(expected_response, self.simulation.book(trip))

        self.simulation.increment_time()
        self.assertIsNone(self.simulation.book(trip))

    def test_increment_time_for_staggered_bookings(self):
        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 5}})
        expected_response = {'car_id': 1, 'total_time': 5}
        self.assertEqual(expected_response, self.simulation.book(trip))
        self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 2}})
        expected_response = {'car_id': 2, 'total_time': 2}
        self.assertEqual(expected_response, self.simulation.book(trip))
        self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 7}})
        expected_response = {'car_id': 3, 'total_time': 7}
        self.assertEqual(expected_response, self.simulation.book(trip))
        self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 2},
                     'destination': {'x': 0, 'y': 6}})
        expected_response = {'car_id': 2, 'total_time': 4}
        self.assertEqual(expected_response, self.simulation.book(trip))
        self.simulation.increment_time()

        self.assertIsNone(self.simulation.book(self.trip))
        self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 5},
                     'destination': {'x': 0, 'y': 10}})
        expected_response = {'car_id': 1, 'total_time': 5}
        self.assertEqual(expected_response, self.simulation.book(trip))
        self.simulation.increment_time()

        self.assertIsNone(self.simulation.book(self.trip))

        for i in range(10):
            self.simulation.increment_time()

        trip = Trip({'source': {'x': 0, 'y': 0},
                     'destination': {'x': 0, 'y': 10}})
        expected_response = {'car_id': 2, 'total_time': 16}
        self.assertEqual(expected_response, self.simulation.book(trip))
        expected_response = {'car_id': 3, 'total_time': 17}
        self.assertEqual(expected_response, self.simulation.book(trip))
        expected_response = {'car_id': 1, 'total_time': 20}
        self.assertEqual(expected_response, self.simulation.book(trip))


if __name__ == '__main__':
    unittest.main()
