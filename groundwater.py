
import numpy as np
import matplotlib.pyplot as plt

#finite volume method for groundwater transients
"""
mathematical groundwater flow and solute transport 
modelling could be used as an efficient and cost-effective 
tool in the investigation and management of groundwater resources.
"""

#Darcy’s law 
# q_s = flow per unit cross-sectional area in direction s
#
# K = hydraulic conductivity
#
# dh_ds = the hydraulic gradient, the difference between 
# hydraulic head at two points / distance between the two 
# points

# Parameters
K = 3.99 * 10 ** -3 #m/s
n = 0.56
alpha = 10**-5 #ms2 kg-1
beta = 4*10**-4 
rho = 1000 #density of water
g = 9.8 #acceleration due to gravity
b = 15 #m, aquifer thickness

S_s = g*rho*(alpha + n*beta)
Lx, Ly = 300, 300  # Domain dimensions
Nx, Ny = 30, 30    # Number of grid cells
dx, dy = Lx / Nx, Ly / Ny  # Grid cell dimensions
S = b*S_s # Storativity
T = b*K   # Transmissivity
dt = 1.0   # Time step
total_time = 100.0  # Total simulation time

# Initial conditions
h = np.ones((Nx, Ny)) * 10.0  # Initial hydraulic head

# Boundary conditions
h[:, -1] = 12.0  # h(300, y, t) = 12 for all y
h[-1, :] = 12.0  # h(x, 300, t) = 12 for all x
h[0, :] = 5.0    # h(x, 0, 0) = 5 for all x

# Main simulation loop
for t in np.arange(0, total_time, dt):
    h_new = h.copy()

    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            # Control Volume Representation
            control_volume = [
                h[i - 1, j - 1], h[i, j - 1], h[i + 1, j - 1],
                h[i - 1, j], h[i, j], h[i + 1, j],
                h[i - 1, j + 1], h[i, j + 1], h[i + 1, j + 1]
            ]

            # Finite Volume Discretization
            dh_dx = (h[i + 1, j] - h[i - 1, j]) / (2 * dx)
            dh_dy = (h[i, j + 1] - h[i, j - 1]) / (2 * dy)

            # Update hydraulic head
            h_new[i, j] += dt * (S / T) * (dh_dx + dh_dy)
    
    # Apply boundary conditions after updating the interior
    h_new[:, -1] = 12.0  # h(300, y, t) = 12 for all y
    h_new[-1, :] = 12.0  # h(x, 300, t) = 12 for all x
    h_new[0, :] = 5.0    # h(x, 0, 0) = 5 for all x

    h = h_new

# Visualization
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)

plt.contourf(X, Y, h, cmap='viridis')
plt.colorbar(label='Hydraulic Head')
plt.title('2D Groundwater Flow Model')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.show()