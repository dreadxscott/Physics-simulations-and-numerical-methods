import math
import numpy as np
import matplotlib.pyplot as plt
from einsteinpy.metric import Schwarzschild
from einsteinpy.geodesic import Geodesic
from einsteinpy.plotting import GeodesicPlotter
from einsteinpy.metric import BaseMetric
from astropy import units as u

def black_hole_mass(radius):
    #returns the mass required to get a black hole of a given radius
    G = 6.6743 * 10**-11 #m3 kg-1 s-2
    c = 299792458.0
    #black hole escape velocity equation
    # 2*G*M/(R*c^2) = 1
    # M = (R*c^2)/2*G

    mass = (radius*c**2)/(2*G)

    return mass

mass_of_earth = 5.972e24 * u.kg  # Use astropy Quantity for mass
mass_satellite =  1000 * u.kg # mass of a satellite in kg
radius_orbit  = 20000 * u.m # radius of the orbit in meters
momentum_satellite = [0.0, 0.0, 1900.0]

a = 0.

# Initial conditions
initial_position = [radius_orbit.to(u.m).value, np.pi/2, 0.0]

coords = Schwarzschild(coords=[0.0, np.pi/2, 0.0], M=mass_of_earth)

# Create a geodesic
geodesic = Geodesic(
    metric="Schwarzschild",
    metric_params =(a,),
    position = initial_position,
    momentum= momentum_satellite,
    coords = coords,
    end_lambda = 2* np.pi #simulate for one orbit
)

#Integrate the geodesic equation
geodesic_trajectory = geodesic.calculate_trajectory() # the underscore is used to trash the additional info

#Create a plotter
plotter = GeodesicPlotter()

#plot the orbit
plotter.plot(geodesic_trajectory, color="blue")

#Show the plot
plotter.show()

