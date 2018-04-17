class Point:
    """Contains the x and y coordinates of a point on a 2D grid.

    Attributes:
        x: An integer x-coordinate of the point.
        y: An integer y-coordinate of the point.
    """

    def __init__(self, x, y):
        """Initializes Point with x and y coordinates.

        Args:
            x: An integer x-coordinate of the point.
            y: An integer y-coordinate of the point.
        """
        self.x = x
        self.y = y


def manhattan_dist(src, dst):
    """Returns the manhattan distance between two Point instances.

    Args:
        src: A Point instance.
        dst: A Point instance.

    Returns:
        An integer of Manhattan distance units between two Point instances.
    """
    return abs(src.x - dst.x) + abs(src.y - dst.y)
