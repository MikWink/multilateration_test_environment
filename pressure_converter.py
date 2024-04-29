import math
import pvlib

class PressureConverter:
    def __init__(self, p0, T0=288.15, g=9.80665, L=-0.0065, R=8.31432, M=0.0289644):
        self.p0 = p0               # sea level standard pressure in Pascals
        self.T0 = T0               # sea level standard temperature in Kelvin
        self.g = g                 # acceleration due to gravity in m/s^2
        self.L = L                 # temperature lapse rate in K/m
        self.R = R                 # specific gas constant for dry air in J/(kg·K)
        self.M = M                 # molar mass of dry air in kg/mol

    def height_at_pressure(self, pressure):
        if pressure <= 0:
            raise ValueError("Pressure must be positive")
        p = abs(pressure)
        T = self.T0 * (p / self.p0)**(-self.R * self.L / (self.g * self.R))
        h = (self.T0 / self.L) * math.log(self.p0 / p) - (self.R * self.T0 / (self.g * self.M)) * (1 - (p / self.p0)**(self.R / self.g * self.L / self.R))
        return h

test = PressureConverter(101325)
print(test.height_at_pressure(101000))
print(pvlib.atmosphere.pres2alt(101000))