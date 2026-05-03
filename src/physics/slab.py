from .base_case import BaseHeatCase

class PlaneWall(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, L):
        V = L
        A = 1 
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.L = L

    @property
    def Lc(self):
        return self.L