

## Pore-scale apps for code developers

 ----------------------------------------------------------------

### See [doc](doc) folder and .md files in each modules directory for further details

 ----------------------------------------------------------------


### Cloning codes

First clone this repository:

`git clone git@github.com:aliraeini/porescale.git`

or 

`git clone https://github.com/aliraeini/porescale.git`

and then update the common modules:

`git submodule update --init  src/script src/include pkgs/zlib pkgs/libtiff src/libvoxel`

Finally to get other codes run any combination of the following commands.

Pore-network model, pnextract and pnflow:

`git submodule update --init  pkgs/hypre src/pnm`

Contact angle:

`git submodule update --init  pkgs/foamx4m src/ContAngle`

Porefoam two-phase flow:

`git submodule update --init  pkgs/foamx4m src/porefoam2f`

Porefoam single-phase flow:

`git submodule update --init  pkgs/foamx4m src/porefoam1f`



### Build from scratch

Instead of running the git commands above, you can run the contents of 
[setup_from_scratch.sh](setup_from_scratch.sh), to generate this 
repository from scratch.

### Build and test

Compilation requires gnu and cmake and a c++ compiler.  Compilation of porefoam and ContactAngle codes additionally requires libscotch-dev and openmpi-dev, in Ubuntu Linux.

Once you have the prerequisites installed, to compile the codes, run `make`, or `make -j` for parallel build. 

To test the compilation run `make test`.


### Contact and References ###

For contacts and references please see the individual modules or visit:    
https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling


