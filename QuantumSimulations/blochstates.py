import numpy as np
import matplotlib.pyplot as plt

# Define the crystal potential
def crystal_potential(x):
    return np.cos(2 * np.pi * x)

# Define the Bloch wave function
def bloch_wave(x, k):
    return np.exp(1j * k * x) * crystal_potential(x)

# Visualization
x_vals = np.linspace(0, 1, 500)  # Spatial grid
k_vals = np.linspace(-np.pi, np.pi, 101)  # Wave vector values in the first Brillouin zone

fig, ax = plt.subplots(figsize=(10, 6))

# Plot crystal potential
ax.plot(x_vals, crystal_potential(x_vals), label='Crystal Potential', linestyle='--', color='black')

# Plot Bloch states for various k values
for k in k_vals:
    bloch_state = bloch_wave(x_vals, k)
    ax.plot(x_vals, np.real(bloch_state) + np.imag(bloch_state), label=f'Bloch State (k={k:.2f})')

ax.set_title('Bloch States in a 1D Crystal')
ax.set_xlabel('Spatial Coordinate')
ax.set_ylabel('Wave Function')
ax.legend()
plt.show()
