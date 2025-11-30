### Pore-Scale Modelling
Flow in porous media occurs is ubiquitous in natural and manufactured settings, from rainfall falling on soil and transpiration in plants, to filling a baby’s nappy and fluid exchange in electrochemical devices, such as electrolysers and fuel cells. Underground, most of the world’s fresh water is held in porous rock and soil, while deeper formations may contain oil and gas; otherwise the pore space is filled with salty water which can be displaced to store carbon dioxide or hydrogen.

The design and management of flow processes in porous media require accurate tools for analysis and modelling. The advent of micron-resolution three-dimensional X-ray imaging has allowed us to image the pore space and the fluids within it. However, how do we make sense of images that often contain 10s of billions of voxels?
This challenge is met through pore-scale modelling.

This repository has been established to facilitate access to all pore-scale modelling codes developed under the supervision of Professor **[Martin Blunt](https://www.imperial.ac.uk/people/m.blunt)** and Dr. **[Branko Bijeljic](https://www.imperial.ac.uk/people/b.bijeljic)** at Imperial College London. Below are the links to each of these repositories, complete with descriptions for each:


<!-- ### **Here are links to the individual code repositories:** ### -->
 
| Repository | Description |
|------------|-------------|
| <div align="center">**[pnextract](https://github.com/ImperialCollegeLondon/pnextract)** </div>| <div align="center"><img src="readme_resources/pnextract.png" width="600"/><br/><strong>Pore Network Extraction from Micro-CT Images of Porous Media</strong></div> |
| <div align="center">**[PoreXtractor](https://github.com/ImperialCollegeLondon/poreOccupancyAnalysis)**</div> | <div align="center"><img src="readme_resources/poreXtractor.jpeg" width="600"/><br/><strong>Analysis Software for Quantification of Pore and Throat Occupancy in 3D Micro-CT Images</strong></div> |
| <div align="center">**[pnflow](https://github.com/ImperialCollegeLondon/pnflow)**</div> | <div align="center"><img src="readme_resources/pnflow.gif" width="400"/><br/><strong>Pore Network Flow Simulation</strong></div> |
| <div align="center">**[OstRipening](https://github.com/ImperialCollegeLondon/OstRipening )**</div> | <div align="center"><img src="readme_resources/OstRipening.gif" width="300"/><br/><strong>Pore Network Flow for Ostwald Ripening Simulation </strong></div> |
| <div align="center">**[Pore-Network-Modeling-of-Polymer-Flows](https://github.com/ImperialCollegeLondon/Pore-Network-Modeling-of-Polymer-Flows )**</div> | <div align="center"><img src="readme_resources/Polymer.jpg" width="300"/><br/><strong>Pore Network Flow for Non-Newtonian Flow Simulation </strong></div> |
| <div align="center">**[Porefoam1f](https://github.com/ImperialCollegeLondon/poreFoam-singlePhase)**</div> | <div align="center"><img src="readme_resources/Porefoam1f.png" width="500"/><br/><strong>Direct Numerical Simulation (DNS) of Incompressible Single Phase Flow on 3D Images of Porous Media Using OpenFOAM Finite-volume Library</strong></div> |
| <div align="center">**[Porefoam2f](https://github.com/ImperialCollegeLondon/porefoam)**</div> | <div align="center"><img src="readme_resources/Porefoam2f.jpg" width="500"/><br/><strong>Direct Numerical Simulation (DNS) of Incompressible Two-phase Flow on 3D Images of Porous Media Using OpenFOAM Finite-volume Library</strong></div> |
| <div align="center">**[ReactiveTransportAnalyser](https://github.com/ImperialCollegeLondon/ReactiveTransportAnalyser)**</div> | <div align="center"><img src="readme_resources/Porefoam2f.jpg" width="500"/><br/><strong>Reactive Transport Analyzer for Reactions in Pore scale</strong></div> |
| <div align="center">**[ContactAngle](https://github.com/ImperialCollegeLondon/ContactAngle)**</div> | <div align="center"><img src="readme_resources/ContactAngle.png" width="350"/><br/><strong>Automatic Measurements of Contact Angle, Interfacial Curvature, and Surface Roughness in Pore-Scale 3D-Images</strong></div> |
| <div align="center">**[relPermCorrection](https://github.com/ImperialCollegeLondon/relPermCorrection)**</div> | <div align="center"><img src="readme_resources/relPermCorrection.jpg" width="500"/><br/><strong>A Novel Method That Corrects Steady-State Relative Permeability Calculations for Inhomogeneous Saturation Profiles Along the Flow Direction</strong></div> |
| <div align="center">**[TangentPcFit](https://github.com/ImperialCollegeLondon/TangentPcFit)**</div> | <div align="center"><img src="readme_resources/TangentPcFit.png" width="500"/><br/><strong>Implementing a Novel Capillary Pressure Model: Fitting Experimentally Measured Data Across Diverse Wettability Conditions</strong></div> |
| <div align="center">**[GGIECN](https://github.com/ImperialCollegeLondon/GGIECN)**</div> | <div align="center"><img src="readme_resources/GGIECN.png" width="500"/><br/><strong>Enhanced Intelligent Segmentation with Grey Scale Image Gradients</strong></div> |
| <div align="center">**[IPWGAN](https://github.com/ImperialCollegeLondon/IPWGAN)**</div> | <div align="center"><img src="readme_resources/IPWGAN.jpg" width="500"/><br/><strong>Porous Media Generation</strong></div> |
| <div align="center">**[DDIM](https://github.com/ImperialCollegeLondon/DDIM)**</div> | <div align="center"><img src="readme_resources/DDIM.png" width="500"/><br/><strong>Multiphase Images Generation</strong></div> |

---

---


## Pore-scale modules for code developers

This repository serves as developer guide for integrating different git 
codes/submodules linked here and contains no code of its own. 


The script [setup_from_scratch.sh](setup_from_scratch.sh) can be used to 
regenerate this repository from scratch. 

You need to 
[set up a ssh key](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) 
and add it to your Github account for the instructions here to work. 
Otherwise you can modify the git commands and replace the all the `git:` addresses 
with corresponding `https:` addresses, if you do not want to push your changes back 
to Github.


 ----------------------------------------------------------------

### See [doc](doc) folder and doc and README files in each modules directory for further details

 ----------------------------------------------------------------


### Cloning codes

----------------------------------------------------------------

To **clone all the modules at once**, which can be time-consuming to compile, run:

`git clone ----recurse-submodules git@github.com:ImperialCollegeLondon/porescale.git`


----------------------------------------------------------------

To cherry-pick the submodules, first **clone this repository:**

`git clone git@github.com:ImperialCollegeLondon/porescale.git`

or 

`git clone https://github.com/ImperialCollegeLondon/porescale.git`

and then **update the common modules:**

`git submodule update --init  src/script src/include pkgs/zlib pkgs/libtiff src/libvoxel`

Finally to get other codes run any combination of the following commands.



Pore-network model, **pnextract and pnflow:**

`git submodule update --init  pkgs/hypre src/pnm`



**Contact angle code:**

`git submodule update --init  pkgs/foamx4m src/ContAngle`



**Porefoam two-phase** flow solver:

`git submodule update --init  pkgs/foamx4m src/porefoam2f`



**Porefoam single-phase** flow solver:

`git submodule update --init  pkgs/foamx4m src/porefoam1f`


----------------------------------------------------------------

### Create from scratch

Instead of running the git commands above, you can run the contents of 
[setup_from_scratch.sh](setup_from_scratch.sh), to generate this 
repository from scratch.


----------------------------------------------------------------

### Build and test

Compilation requires gnu and cmake and a c++ compiler.  Compilation of porefoam and ContactAngle codes additionally requires libscotch-dev and openmpi-dev, in Ubuntu Linux.

Once you have the prerequisites installed, to compile the codes, run `make`, or `make -j` for parallel build. 

To test the compilation run `make test`.


----------------------------------------------------------------

### Contact and References ###

For contacts and references, please visit the individual modules or explore our research group's [Pore-Scale Modelling page](https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling).

Alternatively, contact **Sajjad Foroughi**:
- Email: s.foroughi@imperial.ac.uk
- Additional Email: foroughi.sajad@gmail.com



