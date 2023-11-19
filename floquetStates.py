import numpy as np
import matplotlib.pyplot as plt

# Time-dependent lattice potential
def time_dependent_potential(x, t):
    return np.cos(2 * np.pi * x) * np.cos(2 * np.pi * t)

# Floquet state
def floquet_state(x, t, k):
    return np.exp(1j * k * x) * time_dependent_potential(x, t)

# Visualization
x_vals = np.linspace(0, 1, 500)  # Spatial grid
t_vals = np.linspace(0, 1, 101)  # Time grid
k_val = 2.0  # Wave vector value

fig, ax = plt.subplots(figsize=(10, 6))

# Plot time-dependent lattice potential
ax.plot(x_vals, time_dependent_potential(x_vals, 0), label='Potential at t=0', linestyle='--', color='black')

# Plot Floquet states for various time values
for t in t_vals:
    floquet_state_vals = floquet_state(x_vals, t, k_val)
    ax.plot(x_vals, np.real(floquet_state_vals) + np.imag(floquet_state_vals), label=f'Floquet State (t={t:.2f})')

ax.set_title('Floquet States in a Time-Dependent Lattice')
ax.set_xlabel('Spatial Coordinate')
ax.set_ylabel('Wave Function')
ax.legend()
plt.show()
