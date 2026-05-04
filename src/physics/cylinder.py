from .base_case import BaseHeatCase
import numpy as np

class InfiniteCylinder(BaseHeatCase):
    def __init__(self, k, rho, cp, h, Ti, T_inf, r0, v=None, a=None):
        # Use provided v and a, or calculate defaults
        V = v if v is not None else (np.pi * r0**2)
        A = a if a is not None else (2 * np.pi * r0)
        
        # Store input values
        self.v_input = V
        self.a_input = A
        
        super().__init__(k, rho, cp, h, Ti, T_inf, v=V, a=A)
        self.r0 = r0

    @property
    def Lc(self):
        return self.r0