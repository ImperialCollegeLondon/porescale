## Description of  upscaled results

The direct single-phase flow simulation results are post-processed by `calc_distributions` code and its results are written in a file named **summary_CASENAME.txt**, where case name is the name of the folder in which the simulations are performed, which is in the format of `IMAGENAME-DelP-FLOWDIR`, e.g. `Berea-1-X`.   The  following are short descriptions of various data written in this file:


- `effPorosity`:    	effective (largest connected path) porosity, computed based on the connected path bounding box, not the total image. Bounding box used are also provided in case a different definition is desired.

- `V_pore`:         	pore volume, of connected pores

- `L_x`, `L_y`, `L_z`:   	lengths of connected pores bounding box, in x, y and z directions respectively.

- `K_x`, `K_y`, `K_z`:    	permeability of connected pores, in x, y and z directions respectively.

- `FF_x`, `FF_x`, `FF_x`: 	formation factor of connected pores, in x, y and z directions respectively.

- `DarcyVelocity`:    	Darcy velocity, average of inlet and (=) outlet fluxes divided by L_x*L_y

- `U_D`:     	Darcy velocity, average of inlet and (=) outlet fluxes divided by L_x*L_y

- `DelP`:   	average pressure drop

- `Umax`:    	maximum of magnitude of velocity vector field

- `Re`:     	Reynold number =  rho*VDarcy*sqrt(K)/mu


**Tabular data with header `x=mag(U)/U_D 	 PDF 	 dV/Vdx 	 PDF(log10(x)) 	 dV/Vd(log10(x))`:**   
  
- `x=mag(U)/U_D`:    	x-axis in velocity distribution, magnitude of velocity at bin centres, normalized by Darcy velocity    
- `PDF`:        	probably density function of mag(U)/U_D    
- `dV/Vdx`:    	same as PDF, probably density function of log(mag(U)/U_D), volume weighted but gives same values as PDF above in typical (no sub-resolution porosity) cases.    
- `PDF(log10(x))`:    	probably density function of log(mag(U)/U_D),     
- `dV/Vd(log10(x))`: same as PDF(log10(x)) in typical (no sub-resolution porosity) cases    .

**Tabular data with header `x=U_x/U_D 	 PDF 	 dV/Vdx`:**     

- `x=U_x/U_D`:    	x axis in velocity distribution, x-component of velocity at bin centres, normalized by Darcy velocity    
- `PDF`:        	probably density function of `x=U_x/U_D`    
- `dV/Vdx`:      probably density function of `x=U_x/U_D`, volume weighted.    

**Tabular data with header `x=U_y/U_D 	 PDF 	 dV/Vdx`:**    
Same as `U_x` distribution above, but for y-component of velocity.

**Tabular data with header `x=U_z/U_D 	 PDF 	 dV/Vdx`:**    
Same as `U_x` distribution above, but for z-component of velocity.

**Tabular data with header `x=U_m/U_D dummy 	 PDF 	 dV/Vdx 	 distConstDelCbrtU`:**    
Velocity distributions obtained by binning the velocity in uniform intervals in the domain of cubic-root of velocity.  These can then be plotted more accurately as most velocities are centred near zero.  These data has not been used in any publication, so double-checking for consistency with results above are needed.

- `x=U_m/U_D`:    	Velocity magnitude at bin centres, normalized by Darcy velocity
- `dummy`:        To be ignored, this is just a reminder for lack of testing of these data
- `PDF`:        	probably density function of `x=U_x/U_D`
- `dV/Vdx`:      probably density function of `x=U_x/U_D`, volume weighted
- `distConstDelCbrtU`:    To be ignored

**Tabular data with header `x=U_x/U_D dummy 	 PDF 	 dV/Vdx`:**    
Same as table above for `x=U_m/U_D`, but for x-component of velocity field, `U_x` instead of `U_m`

**Tabular data with header `x=U_y/U_D dummy 	 PDF 	 dV/Vdx`:**    
Same as table above for `x=U_m/U_D`, but for x-component of velocity field, `U_x` instead of `U_m`

**Tabular data with header `x=U_z/U_D dummy 	 PDF 	 dV/Vdx`:**    
Same as table above for `x=U_m/U_D`, but for x-component of velocity field, `U_x` instead of `U_m`

