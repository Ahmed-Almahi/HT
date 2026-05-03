# Quick Reference: Auto-Solver Behavior

## How It Works

The application now automatically chooses the best solving method based on two key parameters:

### Decision Tree

```
START
  ↓
Calculate Biot (Bi = h·Lc/k)
  ↓
Is Bi < 0.1?
  ├─ YES → LUMPED SYSTEM
  │         ├─ Calculate Fo = t/τ
  │         ├─ Is Fo < 0.2?
  │         │  ├─ YES → Use ANALYTIC ✓
  │         │  └─ NO → Use NUMERICAL ✓
  │
  └─ NO → NON-LUMPED SYSTEM
          ├─ Calculate Fo = α·t/Lc²
          ├─ Is Fo < 0.2?
          │  ├─ YES → Use ANALYTIC ✓
          │  └─ NO → Use NUMERICAL ✓
```

## What You See in the UI

### Analysis Info Display
Located below input fields, shows:
```
Bi=0.0327 (lumped) | Fo=0.0185 | Method: ANALYTIC
```

**Reading the display**:
- **Bi=0.0327**: Biot number indicates lumped system (< 0.1)
- **(lumped)**: System classification
- **Fo=0.0185**: Fourier number is small (early transient)
- **Method: ANALYTIC**: Selected method (ANALYTIC or NUMERICAL)

## Export Data Structure

### Excel Output File
**Sheet 1: "Temperature Data"**
| Time (s) | Position (m) | Temperature (°C) |
|----------|-------------|-----------------|
| 0        | 0.000       | 220             |
| 0        | 0.002       | 220             |
| ...      | ...         | ...             |
| 100      | 0.060       | 45.2            |

**Sheet 2: "Metadata"**
| Parameter                        | Value    |
|--------------------------------|----------|
| Geometry                        | Plane Wall |
| Initial Temp (°C)              | 220      |
| Ambient Temp (°C)              | 25       |
| Thermal Conductivity (W/m·K)   | 110      |
| ... (13 more parameters)       | ...      |

## When Each Method Is Used

### ANALYTIC (One-Term Approximation)
✓ Used when **Fourier < 0.2**
- **Why**: Early transient phase, spatial discretization not needed
- **Speed**: < 1ms per point
- **Accuracy**: Very good for Fo < 0.2
- **Formula**: Uses eigenvalues and infinite series (one term approximation)

### NUMERICAL (Implicit Scheme)
✓ Used when **Fourier ≥ 0.2**
- **Why**: Advanced transient, full spatial discretization needed
- **Speed**: 50-200ms per point
- **Accuracy**: Stable for all Fourier numbers
- **Method**: Implicit finite difference (unconditionally stable)

## Common Questions

### Q: Why does my calculation take longer sometimes?
**A**: If Fourier number is ≥ 0.2, it uses numerical method (slower but more accurate). Early times use analytic (instant).

### Q: How do I know if lumped or non-lumped is used?
**A**: Look at the Analysis Info display. If Bi < 0.1, it's lumped. You can also read it from the Metadata sheet in exported Excel.

### Q: Can I force a specific method?
**A**: No, the method is automatically selected. This ensures optimal accuracy and speed for your parameters.

### Q: What does "system type: non-lumped" mean?
**A**: Spatial temperature gradients cannot be ignored. The solution varies with position inside the object.

## Input Parameters Guide

| Parameter | Units | Typical Range | Notes |
|-----------|-------|--------------|-------|
| Thermal Cond (k) | W/m·K | 10-400 | Higher = faster diffusion |
| Density (ρ) | kg/m³ | 1000-8000 | Material dependent |
| Specific Heat (cp) | J/kg·K | 100-2000 | Material dependent |
| Conv Coeff (h) | W/m²·K | 5-10000 | Higher = faster cooling |
| Initial Temp (Ti) | °C | -50 to 1000 | Starting temperature |
| Ambient Temp (T_inf) | °C | -50 to 100 | Environment temperature |
| Characteristic Length | m | 0.001-1.0 | Lc for lumped, r₀ for cylinder/sphere |
| Area (A) | m² | 0.001-10 | Surface area for lumped calc |
| Volume (V) | m³ | 0.00001-1 | Volume for lumped calc |

## Numerical Limits

- **Minimum time**: 0.001 seconds
- **Maximum time**: No limit
- **Minimum temperature**: No limit
- **Maximum Fourier tracked**: 100 (system approaches ambient)
- **Spatial nodes (analytic)**: 30 points
- **Spatial nodes (numerical)**: 50-100 points

## Tips for Best Results

1. **Verify your material properties** - Incorrect k or ρ causes wrong Biot number
2. **Use realistic convection coefficients** - h = 5-10 (natural), h = 50-500 (forced)
3. **Check if lumped is valid** - Biot number should be < 0.1 for lumped assumption
4. **Monitor Fourier number** - Values > 0.2 automatically trigger numerical method
5. **Export multiple cases** - Compare different geometries in Excel

## Performance Tips

- **For quick preview**: Calculate at small time values
- **For export**: Time points are auto-generated (0 to final time)
- **For batch processing**: Export takes ~2-5 seconds for standard cases

---

**Last Updated**: May 2, 2026
**Version**: 2.0
