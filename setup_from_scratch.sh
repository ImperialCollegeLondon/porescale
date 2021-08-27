

#ldconfig -p | grep libjpeg

echo include src/script/Makefile.msRoot > Makefile

mkdir doc # these are temporary fix, docs should be saven in submodules instead
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/pnflow/master/doc/Image.mhd            )
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/pnflow/master/doc/input_pnflow.dat     )
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/pnflow/master/doc/libvoxel_commands.md )
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/poreFoam-singlePhase/master/doc/nomenclature.md )
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/pnflow/master/doc/pnextract_guide.pdf  )
(cd doc && wget https://raw.githubusercontent.com/ImperialCollegeLondon/pnflow/master/doc/pnflow_guide.pdf     )



git init
git submodule add         git@github.com:aliraeini/script.git                            src/script
git submodule add         git@github.com:aliraeini/sirun.git                             src/include
git submodule add         git@github.com:aliraeini/libtiff.git                           pkgs/libtiff     
git submodule add         git@github.com:aliraeini/zlib.git                              pkgs/zlib         
git submodule add         git@github.com:aliraeini/libvoxel.git                          src/libvoxel
git submodule add         git@github.com:aliraeini/hypre.git                             pkgs/hypre
git submodule add -b main git@github.com:ImperialCollegeLondon/pnflow.git                src/pnm
git submodule add         git@github.com:aliraeini/foamxm.git                            pkgs/foamx4m
git submodule add -b main git@github.com:ImperialCollegeLondon/poreFoam-singlePhase.git  src/porefoam1f
git submodule add -b main git@github.com:ImperialCollegeLondon/porefoam.git              src/porefoam2f
git submodule add -b main git@github.com:ImperialCollegeLondon/ContactAngle.git          src/ContAngle  


make -j 

make test

