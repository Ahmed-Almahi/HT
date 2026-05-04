from .base_case import BaseHeatCase

class PlaneWall(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, L, v=None, a=None):
        # Use provided v and a, or calculate defaults
        V = v if v is not None else L
        A = a if a is not None else 1
        
        # Store input values
        self.v_input = V
        self.a_input = A
        
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.L = L

    @property
    def Lc(self):
        return self.L / 2