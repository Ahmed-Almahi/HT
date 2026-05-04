# Transient Heat Conduction Simulator

A Python desktop application for transient heat conduction analysis in plane walls, infinite cylinders, and spheres. Built as an educational tool for heat transfer coursework at Tanta University.

## Features

- **Three geometries**: Plane Wall, Infinite Cylinder, Sphere
- **Automatic solver selection**: uses lumped-capacitance, analytic one-term, or implicit finite-difference methods depending on Biot and Fourier numbers
- **Interactive PyQt5 GUI**: enter parameters, plot temperature response, and view analysis info instantly
- **Excel export**: save temperature results and metadata to `.xlsx`
- **Optional geometry overrides**: specify custom volume or surface area for advanced cases

## Requirements

- Python 3.8+
- PyQt5
- NumPy
- SciPy
- Matplotlib
- Pandas
- openpyxl

## Installation

1. Create a virtual environment:
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

Start the application:
```bash
python main.py
```

Enter the required physical properties and analysis settings, then click **Calculate and Plot**.

### Input Parameters

| Parameter | Description |
|-----------|-------------|
| Thermal Cond (k) | Thermal conductivity (W/m·K) |
| Density (rho) | Density (kg/m³) |
| Specific Heat (cp) | Specific heat capacity (J/kg·K) |
| Conv Coeff (h) | Convection coefficient (W/m²·K) |
| Initial Temp (Ti) | Initial temperature (°C) |
| Ambient Temp (T_inf) | Ambient temperature (°C) |
| Time (sec) | Analysis time in seconds |
| Length (L or r0) | Half-thickness / radius (m) |
| Volume (V) [Optional] | Optional body volume override |
| Surface Area (A) [Optional] | Optional surface area override |

### Supported Geometries

1. **Plane Wall** — infinite slab with conduction through thickness
2. **Infinite Cylinder** — long cylinder with radial heat flow
3. **Sphere** — solid sphere with radial heat flow

### Solver Logic

The app evaluates dimensionless numbers and chooses the appropriate method:

- **Lumped-capacitance model** for Biot number `Bi < 0.1`
- **Analytic one-term solution** for non-lumped cases with `Fo >= 0.2`
- **Implicit finite-difference numerical solver** for non-lumped cases with lower Fourier numbers

### Export Results

Use **Export to Excel (Time Series)** after a calculation to save results in an Excel workbook with:

- `Temperature Data`: temperature at 0.001 m intervals for half and full analysis times
- `Metadata`: geometry, material properties, dimensionless numbers, solver method, and time constant

## Project Structure

```
.
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── src/
    ├── physics/            # Geometry and heat transfer models
    │   ├── base_case.py    # Abstract heat transfer base class
    │   ├── slab.py         # Plane wall geometry
    │   ├── cylinder.py     # Infinite cylinder geometry
    │   ├── sphere.py       # Sphere geometry
    ├── solvers/            # Solver implementations
    │   ├── analytic.py     # Analytic solution formulas
    │   ├── auto_solver.py  # Auto-selection logic
    │   └── numerical.py   # Implicit finite-difference solvers
    └── ui/                 # GUI components
        ├── widgets.py      # Application widgets and controls
        └── styles.qss      # Qt stylesheet
```

## Theory

The application computes transient conduction using:

- Thermal diffusivity: `α = k / (ρ · cp)`
- Biot number: `Bi = h · Lc / k`
- Fourier number: `Fo = α · t / Lc²`

It supports both spatially distributed solutions and lumped-capacitance behavior depending on the case.

## License

Developed for educational purposes at Tanta University.
