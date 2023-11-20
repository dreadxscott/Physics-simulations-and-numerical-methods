import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define the water cycle model
def water_cycle_model(y, t):
    # y[0]: Precipitation
    # y[1]: Evaporation
    # y[2]: Runoff

    # Parameters
    precipitation_rate = 0.02  # Example precipitation rate (arbitrary units)
    evaporation_rate = 0.01    # Example evaporation rate (arbitrary units)
    runoff_coefficient = 0.2   # Example runoff coefficient (portion of precipitation that becomes runoff)

    # Water cycle equations
    dy0dt = precipitation_rate - evaporation_rate - runoff_coefficient * y[0]
    dy1dt = evaporation_rate
    dy2dt = runoff_coefficient * y[0]

    return [dy0dt, dy1dt, dy2dt]

# Initial conditions
initial_conditions = [0, 0, 0]  # Initial values for Precipitation, Evaporation, and Runoff

# Time points
time_points = np.linspace(0, 100, 100)  # Time from 0 to 100 with 100 points

# Solve the water cycle model using odeint from SciPy
solution = odeint(water_cycle_model, initial_conditions, time_points)

# Extracting results
precipitation, evaporation, runoff = solution.T

# Plotting the results
plt.plot(time_points, precipitation, label='Precipitation')
plt.plot(time_points, evaporation, label='Evaporation')
plt.plot(time_points, runoff, label='Runoff')
plt.xlabel('Time')
plt.ylabel('Amount (arbitrary units)')
plt.title('Basic Water Cycle Simulation')
plt.legend()
plt.show()
