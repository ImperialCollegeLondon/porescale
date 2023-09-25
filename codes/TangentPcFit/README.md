# FitTanCapillaryModel

This is a capillary model that we have proposed based on a tangent function:

**J(S<sub>e</sub>) = A + B * tan(π/2 - π * S<sub>e</sub><sup>C</sup>)**

## Model Description

- **S<sub>e</sub>**: The effective saturation, defined as (S<sub>w</sub> - S<sub>wi</sub>) / (1 - S<sub>or</sub> - S<sub>wi</sub>).
- **J(S<sub>e</sub>)**: The Leverett j-function 
- **A, B, and C**: These parameters are used for fitting the model.
- **S<sub>wi</sub> and S<sub>or</sub>**: Residual wetting and non-wetting saturations, which can also be considered as fitting parameters.

## Usage

The input to the code should include lists of Sw (water saturation) and capillary pressure.

## Citing our Work

If you find this code useful and use it in your research or project, please consider citing the following papers that describe the underlying methods and models:


1. [**Sajjad Foroughi, Branko Bijeljic, and Martin J. Blunt. "A Closed-Form Equation for Capillary Pressure in Porous Media for All Wettabilitie." Transport in Porous Media (2022).**](https://doi.org/10.1007/s11242-022-01868-3)



By citing our work, you will help others to understand the foundation of this code and contribute to the recognition of our research efforts.

## Contact and References
If you encounter any issues or have suggestions for improvement, please feel free to raise an issue or submit a pull request. For contacts and references, please see: [**Imperial College London - Pore-Scale Modelling**](https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling) or contact Sajjad Foroughi, email: s.foroughi@imperial.ac.uk or foroughi.sajad@gmail.com.
