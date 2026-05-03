from unittest import result

import numpy as np
from .analytic import solve_one_term_slab, solve_one_term_cylinder, solve_one_term_sphere
from .numerical import solve_implicit_fdm_slab, solve_implicit_fdm_cylinder, solve_implicit_fdm_sphere


class AutoSolver:
    """Auto-selects solution method based on dimensionless numbers."""
    
    THRESHOLD_BIOT = 0.1
    THRESHOLD_FOURIER = 0.2
    
    @staticmethod
    def get_analysis_info(body, t):
        """
        Get analysis info including Biot, Fourier numbers and method selection (analytic or numerical) you will know ali :).
        
        Returns:
            dict: {
                'biot': Biot number,
                'fourier': Fourier number, (the reference say tau or Fo)
                'is_lumped': Boolean (True if Bi < 0.1),
                'use_analytic': Boolean (True if should use analytic),
                'method': 'analytic' or 'numerical',
                'system_type': 'lumped' or 'non-lumped',
                'time_constant': Time constant in seconds (for lumped systems)
            }
        """
        biot = body.get_biot()
        is_lumped = biot < AutoSolver.THRESHOLD_BIOT
        
        # Always calculate spatial Fourier for display/verification
        fourier = body.get_fourier(t)
        
        if is_lumped:
            system_type = 'lumped'
        else:
            system_type = 'non-lumped'
        
        # For method selection: use appropriate Fourier based on system type
        if is_lumped:
            tau = body.get_time_constant()
            fourier_for_method = t / tau if tau > 0 else 0
        else:
            fourier_for_method = fourier
        
        use_analytic = fourier_for_method >= AutoSolver.THRESHOLD_FOURIER
        method = 'analytic' if use_analytic else 'numerical'
        
        return {
            'biot': biot,
            'fourier': fourier,
            'is_lumped': is_lumped,
            'use_analytic': use_analytic,
            'method': method,
            'system_type': system_type,
            'time_constant': body.get_time_constant()
        }
    
    @staticmethod
    def solve(body, pos, t, geometry_type):

        if t <= 0:
            return body.Ti

        Bi = body.get_biot()
        Fo = body.get_fourier(t)

        # Lumped ONLY if Bi < 0.1
        if Bi < 0.1:
            tau = body.get_time_constant()
            return body.T_inf + (body.Ti - body.T_inf) * np.exp(-t / tau)

        # Non-lumped
        if Fo >= 0.2:
            # analytic (one-term)
            if geometry_type == 'slab':
                return solve_one_term_slab(body, pos, t)
            elif geometry_type == 'cylinder':
                return solve_one_term_cylinder(body, pos, t)
            elif geometry_type == 'sphere':
                return solve_one_term_sphere(body, pos, t)
        else:
            # numerical
            dt = min(t / 100, 0.1)
            dt = max(dt, 0.001)

            if geometry_type == 'slab':
                result = solve_implicit_fdm_slab(body, nodes=100, dt=dt, total_time=t)
            elif geometry_type == 'cylinder':
                result = solve_implicit_fdm_cylinder(body, nodes=50, dt=dt, total_time=t)
            elif geometry_type == 'sphere':
                result = solve_implicit_fdm_sphere(body, nodes=50, dt=dt, total_time=t)

            node_idx = int((pos / body.Lc) * (len(result) - 1))
            node_idx = min(max(node_idx, 0), len(result) - 1)

            return result[node_idx]
    
    @staticmethod
    def solve_time_series(body, positions, times, geometry_type):
        """
        Solve for a series of times at given positions.
        
        Args:
            body: Physics object
            positions: Array of positions
            times: Array of times
            geometry_type: 'slab', 'cylinder', or 'sphere' (you can add more if needed)
        
        Returns:
            dict: {
                'times': times array,
                'positions': positions array,
                'temperatures': 2D array [time_idx][pos_idx],
                'analysis': list of analysis info for each time step
            }
        """
        temperatures = []
        analysis_info = []
        
        for t in times:
            temps_at_t = []
            for pos in positions:
                temp = AutoSolver.solve(body, pos, t, geometry_type)
                temps_at_t.append(temp)
            temperatures.append(temps_at_t)
            analysis_info.append(AutoSolver.get_analysis_info(body, t))
        
        return {
            'times': times,
            'positions': positions,
            'temperatures': np.array(temperatures),
            'analysis': analysis_info
        }
