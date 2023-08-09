## Pore Occupancy Analysis:

In this GitHub repository, you will find the code that enables the quantification of pore and throat occupancy in a 3D micro-CT image. The code processes pore network data extracted from dry scan images using a dedicated pore network extraction algorithm. Subsequently, the wet image is mapped onto the extracted network. Please note that the preferred format for wet images is TIFF. This code generates the mapping results and provides the distribution of pores and throats based on the input data. 
This code allows you to perform detailed pore occupancy analysis on wet micro-CT images of porous media. The primary features include:

- **Dominant Phase Identification:** The code identifies and signals the dominant phase within each pore and throat. This data is crucial for deciphering fluid distribution and flow behavior in your porous media.

- **Pore and Throat Size Distributions for Specific Phases:** The code creates distribution charts for pores and throats that contain a specific phase. These charts are plotted against pore and throat radii, offering a clear visual representation of phase distribution in your porous media. It's worth mentioning that both volume-weighted and frequency-based types of distributions can be generated. Tabulated data is also provided for further analysis. 

- **Overall Pore and Throat Distributions:** In addition to specific phase distributions, the code also provides the distribution data for all pores and throats within the extracted network (Both volume-weighted and frequency-based types of distributions can be generated). This is useful for comprehensive network analysis and comparisons between different phases.

## Required Repository

To use this code, you first need to perform pore network extraction. To familiarize yourself with the network extraction process from dry scans, please check out the [**pnextract**](https://github.com/ImperialCollegeLondon/pnextract.git) repository.


## Standalone Software

Included in the repository is a __windows-based standalone software__ inside the [**bin.zip**](https://github.com/ImperialCollegeLondon/porescale/blob/master/codes/poreOccupancyAnalysis/bin.zip) file, which simplifies the entire process. This standalone software does not require any dependencies. A sample porous media file is provided for you to test the software and familiarize yourself with its functionality.

## Usage

To utilize this software effectively, please follow these steps:


**1.** The input image for network extraction should be a segmented dry-scan image, which can be in raw, raw.gz, or TIF format. It must be an 8-bit image, where zero represents pores, and one represents the rest.

**2.** Once you have selected the dry-scan image, you will be prompted to enter image details, including size (Nx * Ny * Nz) and voxel size. The code will automatically insert the image size and voxel size into the MHD file based on the information you provide. 

**3.** If you are dealing with two-phase flow images, they should be in TIF format. Import the TIF file into ImageJ and save it again as a TIF. The software performs optimally with TIF images prepared using ImageJ.

By following these steps, you'll ensure compatibility with our software.






## Citing our Work

If you find this code useful and use it in your research or project, please consider citing the following papers that describe the underlying methods and models:


1. [**Foroughi, Sajjad, et al. "Pore-by-pore modeling, analysis, and prediction of two-phase flow in mixed-wet rocks." Physical Review E 102.2 (2020): 023302.**](https://doi.org/10.1103/PhysRevE.102.023302)
  
2. [**Foroughi, Sajjad, Branko Bijeljic, and Martin J. Blunt. "Pore-by-pore modelling, validation and prediction of waterflooding in oil-wet rocks using dynamic synchrotron data." Transport in Porous Media 138.2 (2021): 285-308.**](https://doi.org/10.1007/s11242-021-01609-y)

By citing our work, you will help others to understand the foundation of this code and contribute to the recognition of our research efforts.

## Contact and References
If you encounter any issues or have suggestions for improvement, please feel free to raise an issue or submit a pull request. For contacts and references please see: https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling or contact Sajjad Foroughi, email: s.foroughi@imperial.ac.uk or foroughi.sajad@gmail.com

