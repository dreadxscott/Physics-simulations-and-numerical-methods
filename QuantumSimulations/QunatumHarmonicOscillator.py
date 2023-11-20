import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.linalg import expm

class QuantumHarmonicOscillator:
    def __init__(self, x_range, num_points, dt):
        self.x_range = x_range
        self.num_points = num_points
        self.dt = dt

        # Initialize the wave function
        self.x_values = np.linspace(x_range[0], x_range[1], num_points)
        self.psi = np.exp(-self.x_values**2 / 2) / np.pi**0.25

    def potential(self, x):
        # Potential energy function for the harmonic oscillator
        omega = 1.0  # Oscillator frequency
        return 0.5 * omega**2 * x**2

    def evolve(self):
        # Time evolution using the Crank-Nicolson method
        psi = self.psi
        dx = self.x_values[1] - self.x_values[0]

        # Construct the Hamiltonian matrix
        H_kinetic = -0.5 / dx**2 * np.eye(self.num_points, k=-1) + \
                     0.5 / dx**2 * np.eye(self.num_points, k=1) + \
                     np.diag(self.potential(self.x_values))

        # Time evolution operator
        U = expm(-1j * H_kinetic * self.dt / 2)

        # Perform time evolution using the Crank-Nicolson method
        psi = np.dot(U, psi)

        self.psi = psi

    def animate(self, num_frames):
            # Animate the evolution of the wave function and save as a GIF
            fig, ax = plt.subplots()

            def update(frame):
                ax.clear()
                ax.plot(self.x_values, np.abs(self.psi)**2)
                ax.set_ylim(0, 0.5)  # Adjust y-axis limit for better visualization
                ax.set_title(f'Time step {frame}')

                self.evolve()

            ani = FuncAnimation(fig, update, frames=num_frames, repeat=False)
            plt.show()

# Instantiate a QuantumHarmonicOscillator
x_range = (-5, 5)
num_points = 200
dt = 0.01
harmonic_oscillator = QuantumHarmonicOscillator(x_range, num_points, dt)

# Animate the evolution for a certain number of frames and save as GIF
num_frames = 100
harmonic_oscillator.animate(num_frames)
