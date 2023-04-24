import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from subprocess import Popen, PIPE, call
from multiprocessing import Pool
from multiprocessing import Process,Value, Array
from scipy.stats import pearsonr
import skimage.io as io
import math
import imageio
from math import pi
import time

from datetime import datetime
import pygmo as pg
import matplotlib as mpl
import numpy as np
import subprocess
import fileinput
import gzip
import shutil
import glob
import zipfile
import sys
import os
import xml.etree.ElementTree as ET

#Description:
'''
This function reads a single tiff image file and extracts the pore and throat location and volume data from the 
corresponding .dat files. It then calculates the dominante lable that filling each pore and throat  
('Value' or 'Label') and optionally performs a volumetric analysis of the element volume for each pore and throat. 
Finally, it saves the histograms of the filling values as PNG files in a subdirectory named after the tiff file.
'''
def readSingleTiffImage(original_path, tif_file_name2_read, phase_index="Value", volumetric='n', element_spacing=1.0, x_direction='z'):
    global SectionPart, SectionPartThroat, NN, tOut1, tOut2, pOut, fExpPore, fExpThroat

    SectionPart = '<PointData>'
    SectionPartThroat = '<CellData Scalars = "ffaz">'

    with os.scandir(original_path) as entries:
        for entry in entries:
            if entry.is_file():
                print(entry.name)
                if entry.name.endswith("_link2.dat"):
                    temp = np.genfromtxt(original_path+entry.name, delimiter="", unpack=True)
                    throat_volume = temp[6, :]
                    tOut2 = temp
                    number_of_throats = len(throat_volume)

                elif entry.name.endswith("_link1.dat"):
                    temp = np.genfromtxt(original_path+entry.name, delimiter="", skip_header=True, unpack=True)
                    throat_radius = temp[3, :]
                    tOut1 = temp

                elif entry.name.endswith("_link3.dat"):
                    f = open(original_path+entry.name)
                    temp = np.loadtxt(f, skiprows=1, usecols=[0, 1, 2, 3])
                    throat_location = temp[:, 1:]
                    f.close()
                elif entry.name.endswith("_node1.dat"):
                    f = open(original_path+entry.name)
                    temp = np.loadtxt(f, skiprows=1, usecols=[0, 1, 2, 3])
                    pore_location = temp[:, 1:]
                    f.close()
                elif entry.name.endswith("_node2.dat"):
                    temp = np.genfromtxt(original_path+entry.name, delimiter="", unpack=True)
                    pore_volume = temp[1, :]
                    pore_radius = temp[2, :]
                    pOut = temp
                    number_of_pores = len(pore_radius)
                elif (entry.name.endswith(".mhd")) and (not entry.name.endswith("_VElems.mhd")):
                    mhd_file_name = entry.name
                    f = open(original_path+entry.name)
                    for line in f:
                        string = line.split()
                        if(len(string) > 0):
                            if (string[0] == 'offset') or (string[0] == 'Offset'):
                                offset_b = [float(string[2]), float(string[3]), float(string[4])]
                            elif (string[0] == 'direction') or (string[0] == 'Direction'):
                                x_direction = string[-1]
                            elif (string[0] == 'elementSpacing') or (string[0] == 'elementspacing') or (string[0] == 'ElementSpacing'):
                                element_spacing = float(string[-1])
                                if element_spacing > 1:
                                    element_spacing *= 1.0e-6


    tiff_counter = 1
    NN = tiff_counter

    fExpPore = np.zeros((number_of_pores, tiff_counter))
    fExpThroat = np.zeros((number_of_throats, tiff_counter))

    VExpPore = np.zeros((number_of_pores, 1))
    SwExpPore = np.zeros((number_of_pores, tiff_counter))

    if x_direction.lower() == 'x':
        z_ind = 2
        y_ind = 1
        x_ind = 0
    elif x_direction.lower() == 'y':
        z_ind = 2
        y_ind = 0
        x_ind = 1
    elif x_direction.lower() == 'z':
        z_ind = 0
        y_ind = 1
        x_ind = 2

    im_array = io.imread(original_path + tif_file_name2_read + '.tif')

    file_name_temp = original_path + tif_file_name2_read
    temp = np.shape(im_array)
    i_file = 0

    if volumetric.lower() == 'y':
        print("VOLUMETRIC ", x_direction)
        for iP in range(number_of_pores):
            fExpPore[iP, i_file] = element_volume(pore_location[iP, :], im_array, z_ind, y_ind, x_ind, offset_b, element_spacing, phase_index, temp, pore_radius[iP])
        for iT in range(number_of_throats):
            fExpThroat[iT, i_file] = element_volume(throat_location[iT, :], im_array, z_ind, y_ind, x_ind, offset_b, element_spacing, phase_index, temp, throat_radius[iT])
    else:
        for iP in range(number_of_pores):
            fExpPore[iP, i_file] = element_centre(pore_location[iP, :], im_array, z_ind, y_ind, x_ind, offset_b, element_spacing, phase_index)
        for iT in range(number_of_throats):
            fExpThroat[iT, i_file] = element_centre(throat_location[iT, :], im_array, z_ind, y_ind, x_ind, offset_b, element_spacing, phase_index)

    if not os.path.isdir(original_path + tif_file_name2_read + '/'):
        os.mkdir(original_path + tif_file_name2_read + '/')

    if os.path.exists(original_path + tif_file_name2_read + '/' + 'fThroats.dat'):
        os.remove(original_path + tif_file_name2_read + '/' + 'fThroats.dat')

    if os.path.exists(original_path + tif_file_name2_read + '/' + 'fPores.dat'):
        os.remove(original_path + tif_file_name2_read + '/' + 'fPores.dat')

    plt.close('all')
    plt.figure(1)
    plt.hist(fExpPore, bins='auto')

    if os.path.exists(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fPores_' + ".png"):
        os.remove(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fPores_' + ".png")
    plt.savefig(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fPores_' + ".png", dpi=100, bbox_inches='tight')

    plt.close('all')
    plt.figure(2)
    plt.hist(fExpThroat, bins='auto')

    
    if os.path.exists(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fThroats_' + ".png"):
        os.remove(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fThroats_' + ".png")
    plt.savefig(original_path + tif_file_name2_read + '/' + tif_file_name2_read + '_fThroats_' + ".png", dpi=100, bbox_inches='tight')

    plt.close('all')
    return fExpPore, fExpThroat
'''
This function takes as input the coordinates of a point in 3D space (xP), an image in 3D (Im), 
and parameters related to the voxel size and offset (a, b, c, Of, dV). It returns the value of the 
voxel in the image that corresponds to the input point (xP) by computing the indices of the voxel 
using the provided parameters and using those indices to access the voxel in the image. 
If an optional phase index is provided, the function returns 1 if the voxel value matches the 
phase index and 0 otherwise.
'''
def elementCentre(xP, Im, a, b, c, Of, dV, phaseIndex="Value"):
    pp = np.int_([0, 0, 0])
    pp[0] = int(math.floor((xP[a] - Of[a]) / dV))  # +offsetB[zIndex]/ElementSpacingT)))
    pp[1] = int(math.floor((xP[b] - Of[b]) / dV))  # +offsetB[yIndex]/ElementSpacingT)))
    pp[2] = int(math.floor((xP[c] - Of[c]) / dV))  # +offsetB[xIndex]/ElementSpacingT)))
    if phaseIndex == "Value":
        return Im[pp[0], pp[1], pp[2]]
    return 1 * (Im[pp[0], pp[1], pp[2]] == phaseIndex)
'''
This function calculates the volume of an element (pore or throat) based on its location and radius within a 3D image. The input parameters are:

xP: an array containing the coordinates of the element in the 3D image.
Im: a 3D numpy array representing the image.
a, b, c: integer values representing the indices of the three axes of the 3D image.
Of: an array containing the offsets of the image in each direction.
dV: the element spacing.
ImSize: an array containing the dimensions of the 3D image.
IR: the radius of the element.
phaseIndex: (optional) the value to be used to identify the element in the image.
The function first calculates the lower and upper limits of the element's position along each 
of the three axes based on its location and radius. It then creates arrays X, Y, and Z 
representing the coordinates of each point within the bounding box of the element. It 
calculates the distance between each point and the center of the element and determines 
which points fall within the element by comparing this distance to the radius. Finally, it 
returns the value of the most common phase (or the specified phase, if provided) within the element.
'''
def elementVolume(xP, Im, a, b, c, Of, dV, ImSize, IR, phaseIndex="Value"):
    iL = int(math.floor((xP[a] - Of[a] - IR) / dV))
    iL = max(0, iL)
    iU = int(math.floor((xP[a] - Of[a] + IR) / dV)) + 2
    iU = min(iU, ImSize[a])
    jL = int(math.floor((xP[b] - Of[b] - IR) / dV))
    jL = max(0, jL)
    jU = int(math.floor((xP[b] - Of[b] + IR) / dV)) + 2
    jU = min(jU, ImSize[b])
    kL = int(math.floor((xP[c] - Of[c] - IR) / dV))
    kL = max(0, kL)
    kU = int(math.floor((xP[c] - Of[c] + IR) / dV)) + 2
    kU = min(kU, ImSize[c])
    iS = iU - iL
    jS = jU - jL
    kS = kU - kL
    temp0 = (np.arange(iL, iU) + 0.5) * dV
    tempVector = np.zeros((iS, 1, 1))
    tempVector[:, 0, 0] = temp0
    temp2Array = np.repeat(tempVector, jS, 1)
    X = np.repeat(temp2Array, kS, 2)
    temp1 = (np.arange(jL, jU) + 0.5) * dV
    tempVector = np.zeros((1, jS, 1))
    tempVector[0, :, 0] = temp1
    temp2Array = np.repeat(tempVector, iS, 0)
    Y = np.repeat(temp2Array, kS, 2)
    temp2 = (np.arange(kL, kU) + 0.5) * dV
    tempVector = np.zeros((1, 1, kS))
    tempVector[0, 0, :] = temp2
    temp2Array = np.repeat(tempVector, iS, 0)
    Z = np.repeat(temp2Array, jS, 1)
    I = Im[iL:iU, jL:jU, kL:kU]
    dMatrix = ((X - (xP[a]-Of[a])) ** 2 + (Y - (xP[b] - Of[b])) ** 2 + (Z - (xP[c] - Of[c])) ** 2) ** 0.5
    dLogical = dMatrix < (IR + 0.5 * dV)
    I = I[:]
    dLogical = dLogical[:]
    counts = np.bincount(I[dLogical])
    return np.argmax(counts)

def plotDistribution(radiusData, weights, fFaz, linePattern, lineWidth, n, pltLabel='_nolegend_', lineStyle='-', markerStyle=None):
    vTotal = np.sum(weights)
    rMax = np.max(radiusData) + 1e-32
    rMin = np.min(radiusData) - 1e-32
    drV = (rMax - rMin) / (n - 1)
    Edges = np.zeros(shape=(n, 1), dtype=float)
   
    fr = np.zeros(shape=(n - 1, 1), dtype=float)
    Edges[0] = rMin
    
    tempArray = (radiusData * fFaz)
    for ii in range(n - 1):        
        rUpper = rMin + (ii + 1) * drV
        rLower = rMin + (ii) * drV
        Edges[ii + 1] = rUpper
        if ii == n - 2:
            rUpper = np.inf

        temp = ((tempArray >= rLower) & (tempArray < rUpper))
       
        fr[ii] = np.sum(weights[temp])
    
    rV = Edges[:n - 1] + np.diff(Edges, axis=0) / 2
    minrV = min(rV)

    rV = np.insert(rV, 0, 0.0)
    fr = np.insert(fr, 0, 0.0)
    rV = np.append(rV, rV[-1] + drV)
    fr = np.append(fr, 0.0)

    xx = rV * 1e6
    yy = fr / (vTotal)

    if minrV * 1e6 > 10:
        xx[0] = minrV * 1e6 - 0.00001

    plt.plot(xx, yy, color=linePattern, linestyle=lineStyle, linewidth=lineWidth, marker=markerStyle, markersize=6, markerfacecolor='None', alpha=1.0, label=pltLabel)

    return xx, yy
def plotPoreAndThroatDist(fileName, nBin=30, DistType='V'):
    print('Inside pore and throat plot!')
    if DistType == 'V':
        poreVolume = pOut[1, :]
        throatVolume = tOut2[6, :]
    elif DistType == 'F':
        poreVolume = np.ones(len(pOut[1, :]))
        throatVolume = np.ones(len(tOut2[6, :]))
    poreRadius = pOut[2, :]
    throatRadius = tOut1[3, :]
    weightPoreVector = np.ones(len(poreRadius))
    binNumber = nBin
    nPlot = -1

    # Plot pore filling distributions
    messagebox.showinfo("Information", "Close the plot to continue.")
    plt.figure(2*(nPlot+1))
    x, y = plotDistribution(poreRadius, poreVolume, weightPoreVector, 'silver', 4, binNumber)
    yp = y
    plt.fill_between(x, 0, y, color='silver', label='_nolegend_')
    poreRadiusMaximimLimit = 1.1 * np.max(x)

    plt.xlim([0, poreRadiusMaximimLimit])
    plt.ylim([0, np.max(y)*1.1])
    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')
    plt.title('Pore size distribution')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16

    fileName = resultsAddress + os.path.basename(fileName)
    png_file_path = fileName + "_pores" + DistType + str(nPlot) + "_" + str(binNumber) + ".png"
    eps_file_path = fileName + "_pores" + DistType + str(nPlot) + "_" + str(binNumber) + ".eps"
    svg_file_path = fileName + "_pores" + DistType + str(nPlot) + "_" + str(binNumber) + ".svg"
    if os.path.exists(png_file_path):
        os.remove(png_file_path)
    plt.savefig(png_file_path)
    if os.path.exists(eps_file_path):
        os.remove(eps_file_path)

    # Plot throat filling distributions
    weightThroatVector = np.ones(len(throatRadius))

    plt.figure(2*(nPlot+1)+1)
    x, y = plotDistribution(throatRadius, throatVolume, weightThroatVector, 'silver', 4, binNumber)
    yt = y
    plt.fill_between(x, 0, y, color='silver', label='_nolegend_')
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y)*1.1])
    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')
    plt.title('Throat size distribution')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16

    png_file_path = fileName + "_throats" + DistType + str(nPlot) + "_" + str(binNumber) + ".png"
    eps_file_path = fileName+"_pores"+DistType+str(nPlot)+"_"+str(binNumber)+".eps"
    svg_file_path = fileName+"_pores"+DistType+str(nPlot)+"_"+str(binNumber)+".svg"
    if os.path.exists(png_file_path):
        os.remove(png_file_path)        
    plt.savefig(png_file_path)
    if os.path.exists(eps_file_path):
        os.remove(eps_file_path)        

    ##################                  Plot Data                     #################
    #'''
    ##########################################################################################
    ##                         Plot throat filling distributions                            ##
    ##########################################################################################

    plt.figure(2*(nPlot+1)+1)
    
    x,y = plotDistribution(throatRadius,throatVolume,weightThroatVector,'silver',4,binNumber)
    yt=y
    plt.fill_between(x,0,y,color='silver', label='_nolegend_')
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y)*1.1])

    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')
    plt.title('Throat size distribution')

    plt.gca().spines['top'].set_visible(False)  
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16
    
    png_file_path = fileName+"_throats"+DistType+str(nPlot)+"_"+str(binNumber)+".png"
    eps_file_path = fileName+"_throats"+DistType+str(nPlot)+"_"+str(binNumber)+".eps"
    svg_file_path = fileName+"_throats"+DistType+str(nPlot)+"_"+str(binNumber)+".svg"
    if os.path.exists(png_file_path):
        os.remove(png_file_path)        
    plt.savefig(png_file_path)
    if os.path.exists(svg_file_path):
        os.remove(svg_file_path)        

    return x, yp, yt
def plotPoreAndThroatDistPhase(fileName, nBin=30, DistType='V', phaseDesired=-1):
    global fExpPore, fExpThroat, pOut, tOut1, tOut2, resultsAddress

    if DistType == 'V':
        poreVolume = pOut[1, :]
        throatVolume = tOut2[6, :]
    elif DistType == 'F':
        poreVolume = np.ones(len(pOut[1, :]))
        throatVolume = np.ones(len(tOut2[6, :]))
    poreRadius = pOut[2, :]
    throatRadius = tOut1[3, :]

    weightPoreVector = (fExpPore == phaseDesired)
    weightThroatVector = (fExpThroat == phaseDesired)

    binNumber = nBin
    nPlot = -1

    # Plot pore size distribution
    plt.figure(2 * (nPlot + 1))
    x, y = plotDistribution(poreRadius, poreVolume, np.ones(len(poreRadius)), 'silver', 4, binNumber)
    xp, yp = plotDistribution(poreRadius, poreVolume, (1 * weightPoreVector).flatten(), 'r', 1, binNumber, 'Phase = ' + str(phaseDesired))
    plt.fill_between(x, 0, y, color='silver', label='_nolegend_')
    poreRadiusMaximimLimit = 1.05 * np.max(x)

    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y) * 1.1])
    plt.xlabel('Radius (${\mu}m$)')
    plt.ylabel('Probability')
    plt.title('Pore size distribution')
    plt.gca().spines['top'].set_visible(False)  
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16

    fileName = resultsAddress + os.path.basename(fileName) + "_" + str(phaseDesired) + "_" + str(binNumber)
    if os.path.exists(fileName + "_pores" + DistType + str(nPlot) + ".png"):
        os.remove(fileName + "_pores" + DistType + str(nPlot) + ".png")        
    plt.savefig(fileName + "_pores" + DistType + str(nPlot) + ".png")
    if os.path.exists(fileName + "_pores" + DistType + str(nPlot) + ".eps"):
        os.remove(fileName + "_pores" + DistType + str(nPlot) + ".eps")        
    


    # Plot throat size distribution
    plt.figure(2 * (nPlot + 1) + 1)
    x, y = plotDistribution(throatRadius, throatVolume, np.ones(len(throatRadius)), 'silver', 4, binNumber)
    xt, yt = plotDistribution(throatRadius, throatVolume, (1 * weightThroatVector).flatten(), 'r', 1, binNumber, 'Phase = ' + str(phaseDesired))

    plt.fill_between(x, 0, y, color='silver', label='_nolegend_')
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y) *
    plt.xlabel('Radius (${\mu}m$)')
    plt.ylabel('Probability')
    plt.title('Throat size distribution')
    plt.gca().spines['top'].set_visible(False)  
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16

    if os.path.exists(fileName + "_throats" + DistType + str(nPlot) + ".png"):
        os.remove(fileName + "_throats" + DistType + str(nPlot) + ".png")        
    plt.savefig(fileName + "_throats" + DistType + str(nPlot) + ".png", dpi=100, bbox_inches='tight')
    if os.path.exists(fileName + "_throats" + DistType + str(nPlot) + ".eps"):
        os.remove(fileName + "_throats" + DistType + str(nPlot) + ".eps")        
    

    return x, yp, yt
def extractPoreAndThroatPhaseDist(logicTempPore, logicTempThroat, originalPath, tifFileName2Read, nBin=30, DistType='V', phaseType='None'):

    if DistType == 'V':
        poreVolume = pOut[1,:]
        throatVolume = tOut2[6,:]
    elif DistType == 'F':
        poreVolume = np.ones(len(pOut[1,:]))
        throatVolume = np.ones(len(tOut2[6,:]))
    poreRadius = pOut[2,:]
    throatRadius = tOut1[3,:]
    
    binNumber = nBin
    nPlot = -1

    xp, yp = extractDistribution(poreRadius, poreVolume, logicTempPore, 'silver', 4, binNumber)
    if not os.path.isdir(originalPath + tifFileName2Read + '/'):
        os.mkdir(originalPath + tifFileName2Read + '/')
    
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+'.txt'):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+'.txt')
    np.savetxt(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+'.txt', np.array([xp,yp]).T, delimiter='\t', header='Desired Phase Pores Radius (um) \t\t Desired Phase Probability')        
    
    xt, yt = extractDistribution(throatRadius, throatVolume, logicTempThroat, 'silver', 4, binNumber)
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+DistType+"_"+phaseType+'.txt'):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+DistType+"_"+phaseType+'.txt')
    np.savetxt(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+DistType+"_"+phaseType+'.txt', np.array([xt,yt]).T, delimiter='\t', header='Desired Phase Throats Radius (um) \t\t Desired Phase Probability')    

    plt.figure(2*(nPlot-1))
    x, y = plotDistribution(poreRadius, poreVolume, np.ones(len(poreRadius)), 'silver', 4, binNumber)

    plt.fill_between(x, 0, y, color='silver', label='_nolegend_')
    poreRadiusMaximimLimit = 1.2*np.max(x)
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y)*1.1])

    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')

    plotDistribution(poreRadius, poreVolume, logicTempPore, 'r', 1, binNumber, 'Desired Phase', markerStyle='o')

    plt.legend()
    plt.gca().spines['top'].set_visible(False)  
    plt.gca().spines['right'].set_visible(False)
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".png"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".png")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".png",dpi=100,bbox_inches='tight')
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".eps"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".eps")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+DistType+"_"+phaseType+".eps",format='eps',bbox_inches='tight') 
    ##################                  Plot Data                     #################
    ##########################################################################################
    ##                     Plot pore and throat radius distributions                       ##
    ##########################################################################################
    plt.close('all')
    plt.figure(2*(nPlot-1))
    x,y = plotDistribution(poreRadius,np.ones(len(poreRadius)),logicTempPore,'r',1,binNumber,'Desired Phase',markerStyle = "o")

    plt.legend()
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y)*1.1])

    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')

    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".png"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".png")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".png",dpi=100,bbox_inches='tight')
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".eps"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".eps")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Pores_'+phaseType+".eps",format='eps',bbox_inches='tight')    

    ##################                  Plot Data                     #################
    ##########################################################################################
    ##                     Plot throat radius distributions                                 ##
    ##########################################################################################
    plt.close('all')
    plt.figure(2*(nPlot-1)+1)
    x,y = plotDistribution(throatRadius,np.ones(len(throatRadius)),logicTempThroat,'r',1,binNumber,'Desired Phase',markerStyle = "o")

    plt.legend()
    plt.xlim([np.min(x), poreRadiusMaximimLimit])
    plt.ylim([np.min(y), np.max(y)*1.1])

    plt.xlabel('Radius (${\mu}m$)');
    plt.ylabel('Probability')

    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".png"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".png")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".png",dpi=100,bbox_inches='tight')
    if os.path.exists(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".eps"):
        os.remove(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".eps")        
    plt.savefig(originalPath + tifFileName2Read + '/'+tifFileName2Read+'_Throats_'+phaseType+".eps",format='eps',bbox_inches='tight')    
    plt.close('all')
