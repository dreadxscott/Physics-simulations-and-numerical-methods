import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.linalg import expm

class QuantumParticleRK:
    def __init__(self, x_range, num_points, dt, hbar, m):
        self.x_range = x_range
        self.num_points = num_points
        self.dt = dt
        self.hbar = hbar
        self.m = m

        # Initialize the wave function
        self.x_values = np.linspace(x_range[0], x_range[1], num_points)
        self.psi = np.exp(-self.x_values**2 / 2) / np.pi**0.25

    def potential(self, x, t):
        # Potential energy function for the harmonic oscillator
        omega = 1.0  # Oscillator frequency
        return 0.5 * omega**2 * x**2

    def schrodinger_rk(self, psi, x, V, t):
        k1 = -1.0j * self.hbar / (2 * self.m) * (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / (x[1] - x[0]) ** 2 + V(x, t) * psi
        k2 = -1.0j * self.hbar / (2 * self.m) * (np.roll(psi + 0.5 * self.dt * k1, -1) - 2 * (psi + 0.5 * self.dt * k1) + np.roll(psi + 0.5 * self.dt * k1, 1)) / (x[1] - x[0]) ** 2 + V(x, t + 0.5 * self.dt) * (psi + 0.5 * self.dt * k1)
        k3 = -1.0j * self.hbar / (2 * self.m) * (np.roll(psi + 0.5 * self.dt * k2, -1) - 2 * (psi + 0.5 * self.dt * k2) + np.roll(psi + 0.5 * self.dt * k2, 1)) / (x[1] - x[0]) ** 2 + V(x, t + 0.5 * self.dt) * (psi + 0.5 * self.dt * k2)
        k4 = -1.0j * self.hbar / (2 * self.m) * (np.roll(psi + self.dt * k3, -1) - 2 * (psi + self.dt * k3) + np.roll(psi + self.dt * k3, 1)) / (x[1] - x[0]) ** 2 + V(x, t + self.dt) * (psi + self.dt * k3)

        # Check for division by zero or very small numbers
        tol = 1e-10
        k1[np.abs(x[1] - x[0]) < tol] = 0
        k2[np.abs(x[1] - x[0]) < tol] = 0
        k3[np.abs(x[1] - x[0]) < tol] = 0
        k4[np.abs(x[1] - x[0]) < tol] = 0

        psi_new = psi + self.dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        # Normalize the wave function
        psi_new /= np.sqrt(np.trapz(np.abs(psi_new)**2, x))

        return psi_new

    def animate(self, num_frames):
        # Animate the evolution of the wave function and save as a GIF
        fig, ax = plt.subplots()

        def update(frame):
            ax.clear()
            ax.plot(self.x_values, np.abs(self.psi)**2)
            ax.set_ylim(0, 1)
            ax.set_title(f'Time step {frame}')

            self.psi = self.schrodinger_rk(self.psi, self.x_values, self.potential, frame * self.dt)

        ani = FuncAnimation(fig, update, frames=num_frames, repeat=False)
        plt.show()

# Instantiate a QuantumParticleRK
x_range = (-5, 5)
num_points = 200
dt = 0.01
hbar = 1.0
m = 1.0
particle_rk = QuantumParticleRK(x_range, num_points, dt, hbar, m)

# Animate the evolution for a certain number of frames and save as GIF
num_frames = 1000
particle_rk.animate(num_frames)
