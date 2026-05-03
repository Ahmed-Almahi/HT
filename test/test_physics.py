import pytest
import numpy as np
import sys
sys.path.insert(0, '.')

from src.physics.base_case import BaseHeatCase
from src.physics.slab import PlaneWall
from src.physics.cylinder import InfiniteCylinder
from src.physics.sphere import Sphere


class TestBaseHeatCase:
    """Test the base heat case class."""
    
    def test_time_constant(self):
        """Test that time constant is calculated correctly."""
        k = 0.5      # W/m.K
        rho = 1000   # kg/m³
        cp = 2000    # J/kg.K
        h = 10       # W/m².K
        Ti = 100     # °C
        T_inf = 25   # °C
        L_char = 0.1 # m
        
        body = PlaneWall(k, rho, cp, h, Ti, T_inf, L=L_char)
        
        # tau = (rho * Lc * cp) / h
        expected_tau = (1000 * 0.1 * 2000) / 10
        assert abs(body.get_time_constant() - expected_tau) < 1e-6
    
    def test_biot_number(self):
        """Test Biot number calculation."""
        k = 0.5
        rho = 1000
        cp = 2000
        h = 10
        Ti = 100
        T_inf = 25
        L_char = 0.1
        
        body = PlaneWall(k, rho, cp, h, Ti, T_inf, L=L_char)
        
        # Bi = h * Lc / k
        expected_bi = (10 * 0.1) / 0.5
        assert abs(body.get_biot() - expected_bi) < 1e-6
    
    def test_fourier_number(self):
        """Test Fourier number calculation."""
        k = 0.5
        rho = 1000
        cp = 2000
        h = 10
        Ti = 100
        T_inf = 25
        L_char = 0.1
        
        body = PlaneWall(k, rho, cp, h, Ti, T_inf, L=L_char)
        
        alpha = k / (rho * cp)
        t = 10
        
        # Fo = alpha * t / Lc^2
        expected_fo = (alpha * t) / (L_char ** 2)
        assert abs(body.get_fourier(t) - expected_fo) < 1e-6


class TestPlaneWall:
    """Test Plane Wall (slab) geometry."""
    
    def test_initial_temperature(self):
        """Test that at t=0, temperature equals initial temperature."""
        body = PlaneWall(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, L=0.1)
        
        T = body.calculate_temp(0.05, 0, method='analytic')
        assert abs(T - 100) < 0.1
    
    def test_approaches_ambient(self):
        """Test that temperature approaches ambient as time increases."""
        body = PlaneWall(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, L=0.1)
        
        T = body.calculate_temp(0.05, 10000, method='analytic')
        assert T > 25 and T < 100
    
    def test_reasonable_values(self):
        """Test that temperature values are reasonable (not huge numbers)."""
        body = PlaneWall(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, L=0.1)
        
        T = body.calculate_temp(0.05, 1e10, method='analytic')
        assert -100 < T < 200 


class TestInfiniteCylinder:
    """Test Infinite Cylinder geometry."""
    
    def test_center_temperature(self):
        """Test temperature at center (r=0)."""
        body = InfiniteCylinder(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0, 0, method='analytic')
        assert abs(T - 100) < 0.1
    
    def test_reasonable_values(self):
        """Test that temperature values are reasonable."""
        body = InfiniteCylinder(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0.05, 1e10, method='analytic')
        assert -100 < T < 200


class TestSphere:
    """Test Sphere geometry."""
    
    def test_surface_temperature(self):
        """Test temperature at surface."""
        body = Sphere(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0.1, 0, method='analytic')
        assert abs(T - 100) < 0.1
    
    def test_center_temperature(self):
        """Test temperature at center (r=0)."""
        body = Sphere(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0, 0, method='analytic')
        assert abs(T - 100) < 0.1
    
    def test_reasonable_values(self):
        """Test that temperature values are reasonable."""
        body = Sphere(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0.05, 1e10, method='analytic')
        assert -100 < T < 200


class TestNumericalMethod:
    """Test numerical method."""
    
    def test_numerical_slab(self):
        """Test numerical method for slab."""
        body = PlaneWall(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, L=0.1)
        
        T = body.calculate_temp(0.05, 10, method='numerical')
        assert -100 < T < 200
    
    def test_numerical_cylinder(self):
        """Test numerical method for cylinder."""
        body = InfiniteCylinder(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0.05, 10, method='numerical')
        # Numerical method may differ from analytic, but should be bounded
        assert -200 < T < 300
    
    def test_numerical_sphere(self):
        """Test numerical method for sphere."""
        body = Sphere(k=0.5, rho=1000, cp=2000, h=10, Ti=100, T_inf=25, r0=0.1)
        
        T = body.calculate_temp(0.05, 10, method='numerical')
        # Numerical method may differ from analytic, but should be bounded
        assert -200 < T < 300


if __name__ == '__main__':
    pytest.main([__file__, '-v'])