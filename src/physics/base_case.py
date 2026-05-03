from abc import ABC, abstractmethod

class BaseHeatCase(ABC):
    def __init__(self, k, rho, cp, h, Ti, T_inf, v, a):
        self.k = k
        self.rho = rho
        self.cp = cp
        self.h = h
        self.Ti = Ti
        self.T_inf = T_inf
        self.v = v
        self.As = a
        
        self.alpha = k / (rho * cp)
        self.time_constant = (self.rho * self.v * self.cp) / (self.h * self.As)

    @property
    @abstractmethod
    def Lc(self):
        pass

    def get_biot(self):
        return (self.h * self.Lc) / self.k

    def get_fourier(self, t):
        return (self.alpha * t) / (self.Lc ** 2)

    def get_time_constant(self):
        return self.time_constant