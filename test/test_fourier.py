from src.physics.slab import PlaneWall

body = PlaneWall(k=50, rho=7800, cp=380, h=120, Ti=20, T_inf=500, L=0.04, V=1, A=1)
print(f'Biot number: {body.get_biot():.6f}')
print(f'Time constant (lumped): {body.get_time_constant():.2f} seconds')
analysis_120s = body.get_analysis_info(120)
print(f'\nAt t=120 seconds:')
print(f'  Fourier (spatial, displayed): {analysis_120s["fourier"]:.6f}')
print(f'  System type: {analysis_120s["system_type"]}')
print(f'  Method: {analysis_120s["method"]}')

alpha = body.alpha
Lc = body.Lc
t_for_35_6 = 35.6 * (Lc**2) / alpha
print(f'\nTo get Fo = 35.6 with Lc=0.04, would need t = {t_for_35_6:.2f} seconds')
