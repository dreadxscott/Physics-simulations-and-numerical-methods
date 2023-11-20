import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class QuantumParticleEuler:
    def __init__(self, x_range, num_points, dt):
        self.x_range = x_range
        self.num_points = num_points
        self.dt = dt

        # Initialize the wave function
        self.x_values = np.linspace(x_range[0], x_range[1], num_points)
        self.psi = np.exp(-(self.x_values - 0.5)**2 / (2 * 0.1**2)) * np.exp(1j * 2 * np.pi * self.x_values)

    def potential(self, x):
        # Potential energy function (simple one-dimensional box potential)
        return np.zeros_like(x)

    def evolve(self):
        # Time evolution using Euler discretization
        psi = self.psi
        dx = self.x_values[1] - self.x_values[0]

        # Construct the kinetic term of the Hamiltonian matrix
        H_kinetic = -2 / dx**2 * np.eye(self.num_points) + \
                     1 / dx**2 * np.eye(self.num_points, k=1) + \
                     1 / dx**2 * np.eye(self.num_points, k=-1)

        # Construct the potential term of the Hamiltonian matrix
        H_potential = np.diag(self.potential(self.x_values))

        # Combine the kinetic and potential terms
        H = H_kinetic + H_potential

        # Time evolution operator
        U = np.exp(-1j * H * self.dt)

        # Perform time evolution using Euler discretization
        psi = np.dot(U, psi)

        # Normalize the wave function
        psi /= np.linalg.norm(psi) 
        
        self.psi = psi

# Inside the QuantumParticleEuler class
    def animate(self, num_frames):
        # Animate the evolution of the wave function and save as a GIF
        fig, ax = plt.subplots()

        def update(frame):
            ax.clear()

            # Evolve the wave function
            self.evolve()

            # Normalize the wave function to have a maximum value of 1
            normalized_psi = np.abs(self.psi) / np.max(np.abs(self.psi))

            # Calculate the probability density
            prob_density = np.abs(normalized_psi)**2

            # Plot the probability density
            ax.plot(self.x_values, prob_density)
            ax.set_ylim(0, 1)
            ax.set_title(f'Time step {frame}')

        ani = FuncAnimation(fig, update, frames=num_frames, repeat=False)
        plt.show()


# Instantiate a QuantumParticleEuler
x_range = (0, 1)
num_points = 100
dt = 0.005
particle_euler = QuantumParticleEuler(x_range, num_points, dt)

# Animate the evolution for a certain number of frames
num_frames = 100
particle_euler.animate(num_frames)
