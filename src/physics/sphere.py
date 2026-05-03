from .base_case import BaseHeatCase
import numpy as np

class Sphere(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, r0):
        # لكل كرة:
        V = (4/3) * np.pi * r0**3
        A = 4 * np.pi * r0**2
        
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.r0 = r0

    @property
    def Lc(self):
        return self.r0