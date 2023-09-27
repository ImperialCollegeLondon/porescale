# FitTanCapillaryModel

This is a capillary model based on a tangent function proposed as follows [1]:

**J(S<sub>e</sub>) = A + B * tan(π/2 - π * S<sub>e</sub><sup>C</sup>)**

## Model Description

- **S<sub>e</sub>**: Effective saturation, defined as (S<sub>w</sub> - S<sub>wi</sub>) / (1 - S<sub>or</sub> - S<sub>wi</sub>).
- **J(S<sub>e</sub>)**: Leverett j-function determined from P<sub>c</sub> using this equation:
  **S<sub>e</sub> = P<sub>c</sub> * √(K / ϕ) / σ**
  Where:
  - K is permeability.
  - ϕ is porosity.
  - σ is surface tension.
- **A, B, and C**: Parameters used for fitting the model.
- **S<sub>wi</sub> and S<sub>or</sub>**: Residual wetting and non-wetting saturations, which can also be considered as fitting parameters.

## Usage

To use this code, provide input lists of Sw (water saturation) and capillary pressure (J-function).

## Citing our Work

If you find this code useful and incorporate it into your research or project, please consider citing the following paper that describes the underlying methods and models:

1. [**Sajjad Foroughi, Branko Bijeljic, and Martin J. Blunt. "A Closed-Form Equation for Capillary Pressure in Porous Media for All Wettabilities." Transport in Porous Media (2022).**](https://doi.org/10.1007/s11242-022-01868-3)

By citing our work, you contribute to the recognition of our research efforts and help others understand the foundation of this code.

## Contact and References

If you encounter issues or have suggestions for improvement, please feel free to raise an issue or submit a pull request. For contacts and references, visit [**Imperial College London - Pore-Scale Modelling**](https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling) or contact Sajjad Foroughi via email: s.foroughi@imperial.ac.uk or foroughi.sajad@gmail.com.
