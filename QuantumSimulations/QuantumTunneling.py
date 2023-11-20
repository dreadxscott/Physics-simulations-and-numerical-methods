import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.linalg import expm

class QuantumParticle:
    def __init__(self, x_range, num_points, dt):
        self.x_range = x_range
        self.num_points = num_points
        self.dt = dt

        # Initialize the wave function
        self.x_values = np.linspace(x_range[0], x_range[1], num_points)
        self.psi = np.exp(-(self.x_values - 0.5)**2 / (2 * 0.1**2)) * np.exp(1j * 2 * np.pi * self.x_values)


    def potential(self, x):
        # Potential energy function for quantum tunneling with a square barrier
        barrier_height = 1.5
        barrier_width = 0.2
        barrier = barrier_height * (np.abs(x - 0.5) < barrier_width / 2)
        return barrier

    def potential_electric_field(self, x, q, E):
        # Potential energy function for an electric field
        return q * E(x)

    def potential_magnetic_field(self, x, q, A):
        # Potential energy function for a magnetic field
        return q * A(x)

    def evolve(self):
        # Time evolution using the Crank-Nicolson method
        psi = self.psi
        dx = self.x_values[1] - self.x_values[0]

        # Construct the kinetic terms of the Hamiltonian matrix
        H_kinetic = -2 / dx**2 * np.eye(self.num_points) + \
                     1 / dx**2 * np.eye(self.num_points, k=1) + \
                     1 / dx**2 * np.eye(self.num_points, k=-1)

        # Construct the potential term of the Hamiltonian matrix
        H_potential = np.diag(self.potential(self.x_values))

        # Combine the kinetic and potential terms
        H = H_kinetic + H_potential

        # Time evolution operator
        U = expm(-1j * H * self.dt / 2)

        # Perform time evolution using the Crank-Nicolson method
        psi = np.dot(U, psi)

        self.psi = psi


    def display(self, frame):
        plt.clf()

        # Plot probability density
        plt.plot(self.x_values, np.abs(self.psi)**2, label='Probability Density')

        # Plot potential barrier (if applicable)
        barrier_height = 1.5
        barrier_width = 0.2
        barrier_values = barrier_height * (np.abs(self.x_values - 0.5) < barrier_width / 2)
        plt.plot(self.x_values, barrier_values, label='Potential Barrier')

        plt.ylim(0, max(np.abs(self.psi)**2))
        plt.title(f'Time step {frame}')
        plt.xlabel('Position')
        plt.ylabel('Probability Density')
        plt.legend()

    def animate(self, num_frames):
        # Animate the evolution of the wave function
        fig, ax = plt.subplots()

        def update(frame):
            self.display(frame)
            self.evolve()

        ani = FuncAnimation(fig, update, frames=num_frames, repeat=False)
        plt.show()

# Instantiate a QuantumParticle
x_range = (0, 1)
num_points = 100
dt = 0.005

# Instantiate a QuantumParticle with a potential barrier
particle_tunneling = QuantumParticle(x_range, num_points, dt)

# Animate the evolution for a certain number of frames
num_frames = 100
particle_tunneling.animate(num_frames)
