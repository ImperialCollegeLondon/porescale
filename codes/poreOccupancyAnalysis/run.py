#Import necessary libraries
import numpy as np
import PoreOccupancyAnalysis
import matplotlib.pyplot as plt
import os

#Address of folder containing tif files
Originalpath = 'tifImages/'

#List of tiff file names to be mapped without tiff extension
fileNameS = ["TiffFileName1","TiffFileName2"]

for file_name in fileNameS:
	print(file_name)
	
	# Read tiff file and extract pore and throat phase information
	pore_phase_dist, throat_phase_dist = PoreOccupancyAnalysis.readSingleTiffImage(Originalpath, file_name)
	phaseIndex = 1 # Set the phase index
	
	# Extract pore and throat phase distribution based on volume
	PoreOccupancyAnalysis.extractPoreAndThroatPhaseDist(pore_phase_dist[:, 0] == phaseIndex, throat_phase_dist[:, 0] == phaseIndex, Originalpath, file_name, nBin=30, DistType='V', phaseType="Water")
	
	# Extract pore and throat phase distribution based on surface area
	PoreOccupancyAnalysis.extractPoreAndThroatPhaseDist(pore_phase_dist[:, 0] == phaseIndex, throat_phase_dist[:, 0] == phaseIndex, Originalpath, file_name, nBin=30, DistType='F', phaseType="Water")	
	
	# Clear variables to free up memory
	del pore_phase_dist, throat_phase_dist
