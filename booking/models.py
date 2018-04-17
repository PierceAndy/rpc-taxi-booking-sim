from .gridsimulation import GridSimulation
from .point import Point
from .trip import Trip


_STARTING_POINT = Point(0, 0)
_NUM_TAXIS = 3
simulation = GridSimulation(_STARTING_POINT, _NUM_TAXIS)


def make(booking):
    return simulation.book(Trip(booking))


def increment_time():
    simulation.increment_time()


def reset():
    simulation.reset()
