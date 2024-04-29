import numpy as np


def calculate_distance(base_station, x_y):
    return np.sqrt((base_station[0] - x_y[0])**2 + (base_station[1] - x_y[1])**2)


class Solver:

    def __init__(self):
        self._initialized = False
        self._x_y = np.zeros(2)

    def init(self, _map):
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def get_guess(self):
        return self._x_y

    def set_init_guess(self, _x_y):
        pass

    def make_init_guess(self):
        pass

    def calculate_error(self, _x_y):
        return calculate_distance(self._x_y, _x_y)

    def run(self):
        self._initialized = False
