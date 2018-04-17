from .point import Point, manhattan_dist


class Trip:
    """Contains the starting and ending locations of a trip.

    Attributes:
        src: A Point instance of the starting location of a trip.
        dst: A Point instance of the ending location of a trip.
    """

    def __init__(self, booking):
        """Initializes Trip with starting and ending locations.

        Args:
            booking: A dict mapping starting (source) and ending (destination)
                locations to x and y coordinates. For example:
                {'source': {'x': 0, 'y': 0}, 'destination': {'x': 1, 'y': 1}}
        """
        self.src = Point(booking['source']['x'],
                         booking['source']['y'])
        self.dst = Point(booking['destination']['x'],
                         booking['destination']['y'])

    def travel_duration(self):
        """Returns the amount of time needed to complete the trip.

        Distance is calculated using the Manhattan distance of the starting and
        ending locations, and it takes 1 time unit to traverse 1 Manhattan
        distance unit.

        Returns:
            An integer of time units needed to complete the trip.
        """
        return manhattan_dist(self.src, self.dst)
