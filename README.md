# Transient Heat Conduction Simulator

A Python-based desktop application for analyzing transient heat conduction in various geometries. Developed for the heat transfer course at Tanta University.

## Features

- **Multiple Geometries**: Support for Plane Wall, Infinite Cylinder, Sphere, Semi-Sphere, and Sphere+Cylinder configurations
- **Analytical Solutions**: Accurate temperature distribution calculations using series solutions
- **Interactive GUI**: User-friendly PyQt5 interface with real-time visualization
- **Excel Export**: Export results to Excel format for further analysis
- **Dynamic Updates**: Delayed update mechanism for smooth user experience

## Requirements

- Python 3.8+
- PyQt5
- NumPy
- SciPy
- Matplotlib
- Pandas
- openpyxl

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Input Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| Thermal Cond (k) | Thermal conductivity (W/m·K) | 110 |
| Density (rho) | Density (kg/m³) | 8530 |
| Specific Heat (cp) | Specific heat capacity (J/kg·K) | 380 |
| Conv. Coeff. (h) | Convection coefficient (W/m²·K) | 60 |
| Initial Temp. (Ti) | Initial temperature (°C) | 220 |
| Ambient Temp. (T_inf) | Ambient temperature (°C) | 25 |
| Time (sec) | Time for analysis (s) | 900 |
| Characteristic Length (L or \frac{i}{b}) | Characteristic length (m) | 0.06 |
| Cylinder Length (L) | Cylinder length (m) | 0.1 |

### Supported Geometries

1. **Plane Wall**: Infinite slab with heat conduction through thickness
2. **Infinite Cylinder**: Long cylinder with radial heat flow
3. **Sphere**: Solid sphere with radial heat flow
4. **Semi-Sphere**: Half-sphere geometry
5. **Sphere + Cylinder**: Combined geometry

### Export Results

Click "Export to Excel" after calculating to save results as an Excel file (.xlsx) containing:
- Temperature Data sheet: Position and Temperature values
- Metadata sheet: Geometry type and Time parameters

## Project Structure

```
.
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── src/
    ├── physics/           # Physics classes for different geometries
    │   ├── base_case.py   # Base class for heat transfer
    │   ├── slab.py        # Plane wall geometry
    │   ├── cylinder.py    # Cylinder geometry
    │   ├── sphere.py      # Sphere geometry
    │   ├── semi_sphere.py # Semi-sphere geometry
    │   └── sphere_cylinder.py # Combined geometry
    ├── solvers/           # Numerical and analytical solvers
    │   ├── analytic.py   # Analytical solutions
    │   └── numerical.py   # Numerical solutions
    └── ui/                # User interface components
        ├── widgets.py     # GUI widgets
        └── styles.qss    # Application styles
```

## Theory

The application solves the transient heat conduction equation using separation of variables and Fourier series solutions. The temperature distribution T(x,t) is calculated based on:

- Thermal diffusivity: α = k/(ρ·cp)
- Biot number: Bi = h·L/k
- Fourier number: Fo = α·t/L²

## License

This project is developed for educational purposes at Tanta University.
