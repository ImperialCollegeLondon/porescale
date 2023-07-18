## relPermCorrection
The Relative Permeability Correction Code is a novel method that corrects steady-state relative permeability calculations for inhomogeneous saturation profiles along the flow direction. Traditionally, relative permeability is determined using Darcy's law on small rock samples, assuming a homogeneous saturation profile and constant capillary pressure. However, these assumptions are rarely accurate due to local inhomogeneities and the capillary end effect, where the wetting phase tends to be retained at the outlet.

Our code introduces an analytical approach to correct relative permeabilities using only the measured pressure drops for various fractional flow values, an estimation of capillary pressure, and the saturation profiles. By applying an optimization routine, the code identifies the range of relative permeability values consistent with the uncertainties in the measured pressure.

A significant advantage of our method is its ability to systematically account for the underestimation of relative permeability caused by assuming a homogeneous saturation profile. This effect is particularly pronounced in media with one strongly wetting phase, exhibiting a noticeable capillary end effect. 


## Citing our Work

If you find this code useful and use it in your research or project, please consider citing the following papers that describe the underlying methods and models:


1. [**Guanglei Zhang, Sajjad Foroughi, Branko Bijeljic, and Martin J. Blunt. "A Method to Correct Steady-State Relative Permeability Measurements for Inhomogeneous Saturation Profiles in One-Dimensional Flow." Transport in Porous Media (2023).**](https://doi.org/10.1007/s11242-023-01988-4)
2. [**Guanglei Zhang, Sajjad Foroughi, Ali Q. Raeini, Martin J. Blunt, and Branko Bijeljic. "The impact of bimodal pore size distribution and wettability on relative permeability and capillary pressure in a microporous limestone with uncertainty quantification." Advances in Water Resources 171 (2023): 104352.**](https://doi.org/10.1016/j.advwatres.2022.104352)


By citing our work, you will help others to understand the foundation of this code and contribute to the recognition of our research efforts.

## Contact and References
If you encounter any issues or have suggestions for improvement, please feel free to raise an issue or submit a pull request. For contacts and references please see: https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling or contact Sajjad Foroughi, email: s.foroughi@imperial.ac.uk or foroughi.sajad@gmail.com
