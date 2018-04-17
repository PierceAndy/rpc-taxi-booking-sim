from sortedcontainers import SortedDict
from .point import manhattan_dist


class GridSimulation:
    """Simulates a taxi booking system on a 2D grid.

    The 2D grid world consists of x and y axis that each fit in a 32 bit
    integer., i.e. -2,147,483,648 to 2,147,483,647. A taxi takes 1 time unit to
    move along the x or y axis by 1 unit. More than 1 taxi can be at the same
    Point at any time.

    The number of simulated taxis and their starting Point locations are
    defined during instantiation. Simulated taxis have IDs, ranging from 1 to
    _NUM_TAXIS, that persist across available and occupied states.

    A taxi's state is determined by which SortedDict its ID is a key in:
    _free_taxis for available taxis, and _occupied_taxis for occupied taxis.
    The two states are mutually exclusive.

    Attributes:
        _STARTING_POINT: A Point instance of where all taxis start from.
        _NUM_TAXIS: An integer number of taxis to simulate.
        _free_taxis: A SortedDict of Taxi IDs of available taxis mapped to
            their current Point locations.
        _occupied_taxis: A SortedDict of Taxi IDs of occupied taxis mapped to
            dictionaries containing travelling data with keys 'destination' and
            'time_left' mapped to the Point location of the taxi's destination
            and integer time left before reaching the destination respectively.
    """

    def __init__(self, starting_point, num_taxis):
        """Initializes simulation with given number of taxis at starting Point.

        Args:
            starting_point: A Point instance of where all taxis start from.
            num_taxis: An integer number of taxis to simulate.
        """
        self._STARTING_POINT = starting_point
        self._NUM_TAXIS = num_taxis
        self._free_taxis = SortedDict()
        self._occupied_taxis = SortedDict()
        self.reset()

    def book(self, trip):
        """Makes a booking with given trip details.

        Assigns the closest available taxi to the customer. If more than one
        taxi qualifies, the taxi with the smallest ID is assigned to the
        customer. An available taxi can be assigned only one booking.

        Booking fails if there are no available taxis, or if the trip is
        invalid, i.e. it starts and ends at the same location.

        Args:
            trip: a Trip instance containing the customer's location and
                destination of the trip to be booked.

        Returns:
            a dictionary if booking succeeds, None otherwise. Dictionary has
            keys 'car_id' and 'total_time', containing the ID of taxi booked,
            and the total time needed for the taxi to travel from its current
            location to pick the customer up at the customer's location and to
            drop the customer off at the customer's destination.
        """
        if not self._free_taxis or trip.travel_duration() == 0:
            return None

        taxi_id, pickup_duration = self._find_closest_free_taxi(trip)
        duration = pickup_duration + trip.travel_duration()
        self._occupy_taxi(trip, taxi_id)
        return {'car_id': taxi_id, 'total_time': duration}

    def increment_time(self):
        """Advances simulation time by 1 time unit.

        Time advancement is simulated by moving every occupied taxi by 1
        distance unit in the x or y-axis. Taxis will travel according to the
        manhattan distance from its current position to its destination, along
        the x-axis first, then the y-axis. Any taxi that has reached its
        destination is made available for further booking.
        """
        taxis_to_free = []
        for taxi_id, travelling in self._occupied_taxis.items():
            if travelling['curr_position'].x < travelling['destination'].x:
                travelling['curr_position'].x += 1
            elif travelling['curr_position'].x > travelling['destination'].x:
                travelling['curr_position'].x -= 1
            elif travelling['curr_position'].y < travelling['destination'].y:
                travelling['curr_position'].y += 1
            elif travelling['curr_position'].y > travelling['destination'].y:
                travelling['curr_position'].y -= 1

            if travelling['curr_position'].x == travelling['destination'].x\
                    and travelling['curr_position'].y == travelling['destination'].y:
                taxis_to_free.append(taxi_id)
        self._free_up_taxis(taxis_to_free)

    def reset(self):
        """Resets simulation to its initial state.

        All taxis are initially available for booking, and start from the same
        Point as defined during instantiation.
        """
        self._initialize_free_taxis()
        self._initialize_occupied_taxis()

    def _find_closest_free_taxi(self, trip):
        pickup_location = trip.src
        closest_taxi_id, shortest_pickup_time = None, float('inf')
        for taxi_id, taxi_location in self._free_taxis.items():
            pickup_time = manhattan_dist(taxi_location, pickup_location)
            if pickup_time < shortest_pickup_time:
                closest_taxi_id = taxi_id
                shortest_pickup_time = pickup_time
        return closest_taxi_id, shortest_pickup_time

    def _free_up_taxis(self, taxis):
        for taxi_id in taxis:
            self._free_taxis[taxi_id] \
                = self._occupied_taxis[taxi_id]['destination']
            del self._occupied_taxis[taxi_id]

    def _occupy_taxi(self, trip, taxi_id):
        self._occupied_taxis[taxi_id] = {'curr_position': trip.src,
                                         'destination': trip.dst}
        del self._free_taxis[taxi_id]

    def _initialize_free_taxis(self):
        self._free_taxis.clear()
        for i in range(self._NUM_TAXIS):
            self._free_taxis[i + 1] = self._STARTING_POINT

    def _initialize_occupied_taxis(self):
        self._occupied_taxis.clear()
