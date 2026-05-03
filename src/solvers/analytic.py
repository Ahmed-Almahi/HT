import numpy as np
from scipy.optimize import fsolve
from scipy.special import j0, j1

def solve_one_term_slab(slab_obj, x, t):
    if t <= 0:
        return slab_obj.Ti
    
    Bi = slab_obj.get_biot()
    Fo = slab_obj.get_fourier(t) 
    
    func = lambda L: L * np.tan(L) - Bi
    lambda1 = fsolve(func, 0.5 if Bi < 1.0 else 1.2)[0]
    
    A1 = (4 * np.sin(lambda1)) / (2 * lambda1 + np.sin(2 * lambda1))
    
    exp_term = np.exp(-(lambda1**2) * Fo)
    
    theta = A1 * exp_term * np.cos(lambda1 * (x / slab_obj.Lc))
    
    return slab_obj.T_inf + theta * (slab_obj.Ti - slab_obj.T_inf)

def solve_one_term_cylinder(cyl_obj, r, t):
    if t <= 0:
        return cyl_obj.Ti
    
    Bi = cyl_obj.get_biot()
    Fo = cyl_obj.get_fourier(t)

    func = lambda L: L * j1(L) - Bi * j0(L)
    lambda1 = fsolve(func, 0.5 if Bi < 1.0 else 1.5)[0]

    A1 = (2 * j1(lambda1)) / (lambda1 * (j0(lambda1)**2 + j1(lambda1)**2))

    exp_term = np.exp(-(lambda1**2) * Fo)

    theta = A1 * exp_term * j0(lambda1 * (r / cyl_obj.Lc))

    return cyl_obj.T_inf + theta * (cyl_obj.Ti - cyl_obj.T_inf)

def solve_one_term_sphere(sphere_obj, r, t):
    if t <= 0:
        return sphere_obj.Ti
    
    Bi = sphere_obj.get_biot()
    Fo = sphere_obj.get_fourier(t)
    
    func = lambda L: L * np.cos(L) - (1 - Bi) * np.sin(L)
    lambda1 = fsolve(func, 0.5 if Bi < 1.0 else 1.5)[0]
    
    A1 = (2 * (np.sin(lambda1) - lambda1 * np.cos(lambda1))) / \
         (lambda1 - np.sin(lambda1) * np.cos(lambda1))
    
    exp_term = np.exp(-(lambda1**2) * Fo)
    
    if r == 0:
        theta = A1 * exp_term
    else:
        ratio = lambda1 * r / sphere_obj.Lc
        sin_term = 1.0 if ratio < 1e-10 else np.sin(ratio) / ratio
        theta = A1 * exp_term * sin_term
    
    return sphere_obj.T_inf + theta * (sphere_obj.Ti - sphere_obj.T_inf)