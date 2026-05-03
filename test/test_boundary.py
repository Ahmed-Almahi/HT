import numpy as np
from src.physics.slab import PlaneWall

A = 0.02
V = 8e-4
k = 110
rho = 8530
cp = 380
h = 120
Ti = 20
T_inf = 500
L_char = 0.04
t_test = 420

body = PlaneWall(k=k, rho=rho, cp=cp, h=h, Ti=Ti, T_inf=T_inf, L=L_char, V=V, A=A)

print("Test Case: Exact Parameters from Screenshot")
print(f"Characteristic Length (L): {body.Lc} m")
print(f"Area (A): {A} m²")
print(f"Volume (V): {V} m³")
print(f"Initial Temp: {body.Ti}°C")
print(f"Ambient Temp: {body.T_inf}°C")
print(f"Biot Number: {body.get_biot():.6f}")
print(f"\nAt time t={t_test} seconds:")

# Test at boundary
analysis = body.get_analysis_info(t_test)
print(f"  Fourier Number (spatial): {analysis['fourier']:.6f}")
print(f"  System Type: {analysis['system_type']}")
print(f"  Method: {analysis['method']}")

# Calculate temperature at various positions
positions_test = [0, 0.01, 0.02, 0.03, 0.04]
print(f"\nTemperature profile at t={t_test}s:")
for pos in positions_test:
    temp = body.calculate_temp(pos, t_test)
    print(f"  Position {pos:.4f}m: {temp:.6f}°C")

# Check if temperature at boundary matches expected value
temp_boundary = body.calculate_temp(L_char, t_test)
print(f"\nBoundary temp at {L_char}m: {temp_boundary:.6f}°C")
print(f"Expected (from user): 228.838346°C")
print(f"Difference: {abs(temp_boundary - 228.838346):.4f}°C")
