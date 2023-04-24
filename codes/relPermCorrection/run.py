import pandas as pd
import numpy as np
import multiprocessing
from joblib import Parallel, delayed


from scipy.signal import savgol_filter
from scipy import stats
import matplotlib.pyplot as plt
from scipy.optimize import minimize,shgo,dual_annealing,differential_evolution,basinhopping
from scipy.interpolate import CubicSpline,interp1d,Akima1DInterpolator,PchipInterpolator


class MyBounds(object):
    ''' 
    bounds class to make sure your variable is with in the expected bounds
    '''
    def __init__(self, xmin, xmax):
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)

    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmax and tmin

# Bounds:
lower_bounds = [  0,   0,    0,    0,   0,    0,   0]
upper_bounds = [  1,   1,    1,    1,   1,    1,   1]
my_bounds    = MyBounds(lower_bounds, upper_bounds)


#'''
# Sample length:
L = 0.0516         				# m 
Delta_x = L/3000   				# m
LNew = L           
#'''



consider_fw=np.array([True,True,True,True,True,True,True])
#'''

# Oil Density:
rhoOil = 730        	 # kg/m3

# Oil viscosity:
muOil = 0.00296     	 # Pa.s

# Water Density:
rhoWater = 1218.55  	 # kg/m3

# Water Viscosity:
muWater = 0.00093   	 # Pa.s

# gravitational acceleration:
g = 9.8             	 # m/s2
IncludeGravity = 0;#1
# Permeability:
K = 1.47E-12        	 # m2

# Total Flow Rate:
qt = 1.1411675627685E-05 # m/s

# Water Fractional Flow:
fw = np.array([0.0, 0.05, 0.15, 0.30, 0.50, 0.85, 1.0])
fw = fw[consider_fw]
Nfw = len(fw)-1

# Inlet Capillary Pressure:
Pc = 1000*np.array([3.19584815802796,2.56498909270457,2.54267145726145,2.38963891737797,2.30075413611575,2.373854099684,2.21817793536285]) #Pa WW
PcInlet  = Pc[consider_fw]
PcOutlet = 0*PcInlet
# Pressure Difference:
DeltaP = 1000*np.array([1.75,6.51,7.27,8.65,9.42,10.8,5.94]) # Pa
DeltaP =DeltaP[consider_fw]
DeltaP /=L

# Average Saturation:
SWEXP = np.array([0.144,0.461,0.481,0.518,0.527,0.575,0.617])
SWEXP =SWEXP[consider_fw]

# Saturtion Profile:
a = (pd.read_excel('WWBen_newSw2.xlsx'))
Sws = a.to_numpy()
Sws = Sws[:,consider_fw[:]]

########################################################################

SWEXP[:] = np.mean(Sws,axis=0)
SWEXPMean = np.mean(Sws,axis=0)

Swi = 0.13603131447
SoR = 1.0-0.6982



SWEXP[0] = Swi-1e-16
SWEXP[-1] = 1-SoR+1e-16
SWEXP = np.linspace(SWEXP[0], SWEXP[-1], num=len(SWEXP))

# Average Relative Error in Pressure Difference for Oil Phase:
def OF(x):
	y=np.append(x,0)
	cs = CubicSpline(SWEXP, y, bc_type='natural',extrapolate = True)
	DeltaP_Calc = np.zeros(Nfw)
	for i in range(Nfw):
		DeltaP_Calc[i]=muOil*(1-fw[i])*qt/K*np.sum(1/cs(Sws[:,i]))*Delta_x+IncludeGravity*rhoOil*g*L
	myPenalty = np.sum(x[1:]-x[:-1]>0)
	return np.linalg.norm((DeltaP_Calc/LNew-DeltaP[:-1])/DeltaP[:-1],ord=1)+1.0e16*myPenalty

# Average Relative Error in Pressure Difference for Water Phase:	
def OFWater(x):
	y=np.insert(x,0,0)
	cs = CubicSpline(SWEXP, y, bc_type='natural',extrapolate = True)
	#cs = interp1d(SWEXP, y,kind = 'quadratic',fill_value='extrapolate')
	DeltaP_Calc = np.zeros(Nfw)
	for i in range(Nfw):
		DeltaP_Calc[i]=muWater*(fw[i+1])*qt/K*np.sum(1/cs(Sws[:,i+1]))*Delta_x+IncludeGravity*rhoWater*g*L+PcInlet[i+1]-PcOutlet[i+1]
	myPenalty = np.sum(x[1:]-x[:-1]<0)
	return np.linalg.norm((DeltaP_Calc/LNew-DeltaP[1:])/DeltaP[1:],ord=1)+1.0e16*myPenalty
	
plotCounter = 0

b1 = (0,1)
b2 = (1,6)
bnds = (b1,b2)

Swplot = np.linspace(Swi,1-SoR,100)

# kro Based on assuming a homogenous saturation profile for each fw:
krO0 = np.array([0.686,0.175,0.140,0.097,0.064,0.017,0.000])

x0=krO0[:-1]

OFCriteriaOil = 1.0#(OF(x0))

# Bounds & Constrants:

def constraint1(x):
	return 	x[0]-x[1]
def constraint2(x):
	return 	x[1]-x[2]
def constraint3(x):
	return 	x[2]-x[3]
def constraint4(x):
	return 	x[3]-x[4]
def constraint5(x):
	return 	x[4]-x[5]
def constraint6(x):
	return 	x[5]-x[6]

print("IG = ",x0)
print(OF(x0))

b1 = (0,1)

bnds = (b1,b1,b1,b1,b1,b1)
con1 = {'type':'ineq','fun':constraint1}
con2 = {'type':'ineq','fun':constraint2}
con3 = {'type':'ineq','fun':constraint3}
con4 = {'type':'ineq','fun':constraint4}
con5 = {'type':'ineq','fun':constraint5}
con6 = {'type':'ineq','fun':constraint6}
cons=[con1,con2,con3,con4,con5]


print("##################################################################")

# Number of Realisation:
nPlot = 500

global AllKrOil, AllKrWater,OF_Oil,OF_Water,nRunOil

AllKrOil= np.zeros((len(SWEXP)+1,nPlot))
OF_Oil = np.zeros(nPlot)

# krw Based on assuming a homogenous saturation profile for each fw:

krw0 = np.array([0.000,0.003,0.008,0.014,0.021,0.031,0.067])

x0=krw0[1:]
OFCriteriaW = 1.0 # OFCriteriaW(x0)
AllKrWater= np.zeros((len(SWEXP)+1,nPlot))
OF_Water = np.zeros(nPlot)
nRunOil = 0

# Oil Objective function minimizer:

def myMinimizer(i):

    print(i)

    plotCounter=0
    while(plotCounter<1):
        mySeed = np.random.randint(i*1e6, (i+1)*1e6)

        sol= differential_evolution(OF, bounds=bnds,maxiter=5000,seed=mySeed)   
        
        if(OF(sol.x)<OFCriteriaOil/2):
            print("mySeed = ", mySeed)
            krOil = np.append(sol.x,0)

            cs = PchipInterpolator(SWEXP, krOil)
            krOil[:-1] = cs(SWEXPMean[:-1])             
            print("krOil = ", krOil,"OFOil = ", OF(sol.x ))

            OF_Oil[i]     = OF(sol.x)
            plt.plot(SWEXP ,krOil,color = 'silver')
            
            return np.append(krOil,OF(sol.x))

# Water Objective function minimizer:

def myMinimizerW(i):
    print(i)

    plotCounter=0
    while(plotCounter<1):

        mySeed = np.random.randint(i*1e6, (i+1)*1e6)

        sol= differential_evolution(OFWater, bounds=bnds,maxiter=5000,seed=mySeed)

        if(OFWater(sol.x)<OFCriteriaW):
            krWater = np.insert(sol.x,0,0)
            cs = PchipInterpolator(SWEXP, krWater)
            krWater[1:] = cs(SWEXPMean[1:])
            print("krWater = ", krWater,"OFWater = ", OFWater(sol.x ))

            OF_Water[i]     = OFWater(sol.x)
            plt.plot(SWEXP ,krWater,color = 'silver')

            return np.append(krWater,OFWater(sol.x))

# Parallel Optimization:

print("Number of processors: ", multiprocessing.cpu_count())

num_cores = multiprocessing.cpu_count()-1

if __name__ == "__main__":
    AllKrOil = Parallel(n_jobs=num_cores)(delayed(myMinimizer)(i) for i in range(nPlot))

if __name__ == "__main__":
    AllKrWater = Parallel(n_jobs=num_cores)(delayed(myMinimizerW)(i) for i in range(nPlot))    


np.savetxt("AllKrOil.txt",np.transpose(AllKrOil))
np.savetxt("AllKrWater.txt",np.transpose(AllKrWater))

