from .base_case import BaseHeatCase
import numpy as np

class InfiniteCylinder(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, r0):
        V = np.pi * r0**2
        A = 2 * np.pi * r0
        
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.r0 = r0

    @property
    def Lc(self):
        return self.r0