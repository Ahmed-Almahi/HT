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

    def eigen_eq(L):
        return 1 - L / np.tan(L) - Bi

    lambda1 = fsolve(eigen_eq, 1.0)[0]
    lambda2 = fsolve(eigen_eq, 4.0)[0] 

    def compute_A(L):
        denom = L - np.sin(L) * np.cos(L)
        if abs(denom) < 1e-8:
            return 1.0
        return (2 * np.sin(L)) / denom

    A1 = compute_A(lambda1)
    A2 = compute_A(lambda2)

    term1 = A1 * np.exp(-(lambda1**2) * Fo)
    term2 = A2 * np.exp(-(lambda2**2) * Fo)

    def spatial(L):
        if r == 0:
            return 1.0
        ratio = L * r / sphere_obj.Lc
        return np.sin(ratio) / ratio

    theta = term1 * spatial(lambda1) + term2 * spatial(lambda2)

    theta = max(0.0, min(theta, 1.0))

    return sphere_obj.T_inf + theta * (sphere_obj.Ti - sphere_obj.T_inf)