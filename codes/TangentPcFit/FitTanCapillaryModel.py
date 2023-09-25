
import numpy as np
from scipy.optimize import curve_fit,minimize
import matplotlib.pyplot as plt
from scipy.optimize import dual_annealing, differential_evolution

def myOF1(x):
    global x_data, y_data
    A = x[0]
    B = x[1]
    C = x[2]
    
    # Normalize x_data
    SwMin = x[3]
    SwMax = x[4]

    SwRange = x_data>-1
    
    x_data_normalized = (x_data - SwMin) / (SwMax - SwMin)
    
    #x_data_normalized = x_data_normalized
    y_data1 = y_data

    yCalc = A + B * np.tan(np.pi / 2 - np.pi * x_data_normalized**C)
    


    # Calculate custom weights based on the distance from the middle (0.5)
    distance_from_middle = np.abs(x_data_normalized - 0.5)**1
    max_distance = np.max(distance_from_middle)
    weights = 1.0 #- distance_from_middle / max_distance
    
    # Calculate the weighted mean absolute relative error
    relative_error = np.mean(weights**1 * np.abs((yCalc - y_data1) / y_data1))
    
    # Calculate Mean Squared Error (MSE)
    #mse = np.mean(weights**1 *((yCalc - y_data)/np.mean(y_data))**2)
    mse = np.mean(weights**1 *np.sqrt(((yCalc - y_data1)/np.mean(y_data1))**2))    
    # Add a regularization term (L2 regularization)
    lambda_reg = 0.01  # Adjust the regularization strength
    regularization_term = lambda_reg * (A**2 + B**2 + C**2)
    
    # Combine relative error and MSE, and add regularization
    objective_value = relative_error + mse + regularization_term
    
    return objective_value
def cf_OF(x, A, B, C):
    
    return A + B * np.tan(np.pi/2 - np.pi * x**C)


data = np.loadtxt("Data.txt")
# drainage part of data
logicalDrainage = (data[1:,0]-data[:-1,0])>0
   
# Find the index of the first True element
first_true_index = np.argmax(logicalDrainage)

# Add a True element right after the first True element
logicalDrainage = np.insert(logicalDrainage, first_true_index + 1, True)
    
x_data = data[logicalDrainage,0]  # First column
y_data = data[logicalDrainage,1]  # Second column

# Fit the data to the custom function
initial_guess = [0.5, 1.0, 1.0,0.99*min(x_data),1.01*max(x_data)]  # Initial guess for parameters A, B, and C

# Define the bounds for the parameters A, B, and C, SwMin and SwMax
bounds = [(-10, 10), (0, 20), (0, 10), (0.0*min(x_data), 1.0*min(x_data)), (max(x_data), 1)]  # Adjust the bounds as needed

# Number of Latin Hypercube samples
num_samples = 1000

# Generate a Latin Hypercube sample from the parameter space
lhs_samples = np.zeros((num_samples, len(bounds)))

for i, (min_val, max_val) in enumerate(bounds):
    lhs_samples[:, i] = np.random.uniform(min_val, max_val, num_samples)

# Initialize variables to store the best result
best_initial_guess = None
best_obj_value = float('inf')

# Evaluate the objective function for each sample and select the best one
for i in range(num_samples):
    initial_guess = lhs_samples[i]
    obj_value = myOF1(initial_guess)  # Evaluate the objective function
        
    # Check if this is the best result so far
    if obj_value < best_obj_value:
        best_initial_guess = initial_guess
        best_obj_value = obj_value
    
# Perform differential_evolution optimization
# You can use best_initial_guess as the starting point for optimization
result = differential_evolution(myOF1, bounds, x0=best_initial_guess, maxiter=5000)
    
# Extract the optimized parameters
A_fit, B_fit, C_fit, SwMin,SwMax = result.x

# Generate the curve using the fitted parameters
x_data  = data[logicalDrainage,0]
xx = np.linspace(min(x_data),max(x_data),1000)
xn = (xx-SwMin)/(SwMax-SwMin)
    
    
y_fit = cf_OF(xn, A_fit, B_fit, C_fit)

# Plot the original data and the fitted curve
plt.scatter(data[logicalDrainage,0], y_data,s=10, c='red', marker='o', label='Data')
plt.plot(xx, y_fit, 'g', label='Fitted Model to Data',linewidth=2.5)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

plt.yscale('log')  # Set the y-scale to logarithmic
plt.legend()



########################################################################
########################################################################
plt.xlabel('Wetting phase saturation')
plt.ylabel('Leverett J-function')
plt.yscale('log')
plt.ylim([0.1*min(y_data), 10*max(y_data)])
plt.legend()
ax = plt.gca()
plt.legend(frameon=False)
plt.xlim([0,1.03])  

# Increase font size and make it bold
legend = plt.legend(frameon=False,loc=1)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()+legend.get_texts()):
	item.set_fontsize(14)
	item.set_weight('bold')
    # Remove right and top spines

    # Increase the thickness of the axes
for axis in ['top', 'bottom', 'left', 'right']:
	ax.spines[axis].set_linewidth(2)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)



# Set labels
label_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'bold'}
ax.set_xlabel(r'Wetting Phase Saturation', **label_font)
ax.set_ylabel(r'Leverett J-function', **label_font, rotation=90)
plt.tight_layout()
# Save the figure with a high resolution (300 dpi)
plt.savefig('J.png', dpi=300)  
# Close all open figures
plt.close('all')
