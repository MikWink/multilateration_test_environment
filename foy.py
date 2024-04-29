import sys

import numpy as np

from solver import solver
from solver.solver import Solver


class Foy(Solver):

    def __init__(self):
        super().__init__()
        self._h = np.zeros(2)
        self._G = np.zeros((2, 2))
        self._R_i = None
        self._R_i_1 = None
        self._base_stations = None
        self._treshold = 0.1
        self._max_steps = 20
        self._steps = 0
        pass

    def init(self, _map):
        super().init(_map)
        self._base_stations = _map.get_base_stations()
        self._R_i_1 = _map.get_tdoa_s()
        self._steps = 0
        for bs in self._base_stations:
            print(f"BS: {bs}")

        print(f"R_i_1: {self._R_i_1}")

    def set_init_guess(self, _x_y):
        self._x_y = _x_y
        self._steps = 0

    def make_init_guess(self):
        center = np.sum(self._base_stations, axis=0) / 3
        self._x_y = 650745.995, 5479748.09
        self._steps = 0

    def set_treshold(self, _treshold):
        self._treshold = _treshold

    def set_max_steps(self, _max_steps):
        self._max_steps = _max_steps

    def calculate_R(self):
        for bs in self._base_stations:
            print(f"BS before R_i_guess calculation: {bs}")
        self._R_i = np.array([solver.calculate_distance(base_station, self._x_y)
                              for base_station in self._base_stations])
        print(f"x_y for calculation: {self._x_y}")
        print(f"R_i_guess: {self._R_i}")

    def calculate_G(self):
        self._G[0, 0] = ((self._base_stations[0][0] - self._x_y[0]) / self._R_i[0]) - (
                (self._base_stations[1][0] - self._x_y[0]) / self._R_i[1])
        self._G[0, 1] = ((self._base_stations[0][1] - self._x_y[1]) / self._R_i[0]) - (
                (self._base_stations[1][1] - self._x_y[1]) / self._R_i[1])
        self._G[1, 0] = ((self._base_stations[0][0] - self._x_y[0]) / self._R_i[0]) - (
                (self._base_stations[2][0] - self._x_y[0]) / self._R_i[2])
        self._G[1, 1] = ((self._base_stations[0][1] - self._x_y[1]) / self._R_i[0]) - (
                (self._base_stations[2][1] - self._x_y[1]) / self._R_i[2])
        print(f"G: {self._G}")

    def calculate_h(self):
        self._h[0] = self._R_i_1[1] - (self._R_i[1] - self._R_i[0])
        self._h[1] = self._R_i_1[2] - (self._R_i[2] - self._R_i[0])
        print(f"h: {self._h}")

    def update_x_y(self):
        GT_G = np.matmul(np.transpose(self._G), self._G)

        if np.linalg.cond(GT_G) < 1 / sys.float_info.epsilon:
            GT_G_inv = np.linalg.inv(GT_G)
        else:
            # G is singular matrix -> no convergence
            return False

        GT_G_inv_GT = np.matmul(GT_G_inv, np.transpose(self._G))
        delta_x_y = np.matmul(GT_G_inv_GT, self._h)

        self._x_y = np.add(self._x_y, delta_x_y)
        print(f"Delta x_y: {delta_x_y}")
        return delta_x_y

    def run(self):
        super().run()
        if self._steps == 0:
            delta_abs = np.infty

        self._steps += 1
        self.calculate_R()
        self.calculate_h()
        self.calculate_G()

        delta_x_y = self.update_x_y()
        if isinstance(delta_x_y, bool) and not delta_x_y:
            # no convergence
            return False
        else:
            delta_abs = np.sum(np.abs(delta_x_y))

        # print("Foy-Solver> Step " + str(self._steps) + " | delta: " + str(delta_abs))

        if self._steps > self._max_steps:
            return False
        elif delta_abs > self._treshold:
            return True
        else:
            return self._x_y
