In this GitHub repository, you will find the code that enables the quantification of pore and throat occupancy in a 3D micro-CT image. The code processes pore network data extracted from dry scan images using a dedicated pore network extraction algorithm. 

Subsequently, the wet image is mapped onto the extracted network. Please note that the preferred format for wet images is TIFF.

This code generates the mapping results and provides the distribution of pores and throats based on the input data. 

Included in the repository is a __windows-based standalone software__ inside the zip file, which simplifies the entire process. This standalone software does not require any dependencies. A sample porous media file is provided for you to test the software and familiarize yourself with its functionality.



## Required Repository

To use this code, you first need to perform pore network extraction. To familiarize yourself with the network extraction process from dry scans, please check out the [**pnextract**](https://github.com/ImperialCollegeLondon/pnextract.git) repository.



## Citing our Work

If you find this code useful and use it in your research or project, please consider citing the following papers that describe the underlying methods and models:


1. [**Foroughi, Sajjad, et al. "Pore-by-pore modeling, analysis, and prediction of two-phase flow in mixed-wet rocks." Physical Review E 102.2 (2020): 023302.**](https://doi.org/10.1103/PhysRevE.102.023302)

2. [**Foroughi, Sajjad, Branko Bijeljic, and Martin J. Blunt. "Pore-by-pore modelling, validation and prediction of waterflooding in oil-wet rocks using dynamic synchrotron data." Transport in Porous Media 138.2 (2021): 285-308.**](https://doi.org/10.1007/s11242-021-01609-y)


By citing our work, you will help others to understand the foundation of this code and contribute to the recognition of our research efforts.
