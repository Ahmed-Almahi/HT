from .base_case import BaseHeatCase

class PlaneWall(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, L):
        # لكل وحدة مساحة:
        V = L          # volume per unit area
        A = 1          # surface area per unit area
        
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.L = L

    @property
    def Lc(self):
        return self.L