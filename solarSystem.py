import math
import numpy as np
import scipy
import pandas as pd
import pygame

pygame.init()

(width, heigh) = (500,500)

#Define the mass of the Sun, as well as the gravitational constant
mass_Sol = 1.98 * 10**30  #Mass of the Sun in kilograms
grav_const = 6.67 * 10**-11 #Gravitational Constant G

# Define the masses and distances for the planets
mass_Mercury = 3.3011 * 10**23  # Mass of Mercury in kilograms
dist_Mercury = 5.791 * 10**10  # Distance of Mercury from the Sun in meters

mass_Venus = 4.867 * 10**24  # Mass of Venus in kilograms
dist_Venus = 1.082 * 10**11  # Distance of Venus from the Sun in meters

mass_Earth = 5.972 * 10**24  # Mass of Earth in kilograms
dist_Earth = 1.496 * 10**11  # Distance of Earth from the Sun in meters

mass_Mars = 6.417 * 10**23  # Mass of Mars in kilograms
dist_Mars = 2.279 * 10**11  # Distance of Mars from the Sun in meters

mass_Jupiter = 1.899 * 10**27  # Mass of Jupiter in kilograms
dist_Jupiter = 7.785 * 10**11  # Distance of Jupiter from the Sun in meters

class Planet:
    def __init__(self, mass, distance, angle, velocity):
        self.mass = mass
        self.distance = distance #distance from the Sun
        self.velocity = velocity #orbital velocity
        self.angle = angle #polar coordinate used for this sim
    
    def get_velocity(self, distance, mass):
        self.velocity = math.sqrt(grav_const * (self.mass+mass_Sol) * self.distance)

# Create instances of the Planet class for each planet
mercury = Planet(mass_Mercury, dist_Mercury, angle=0)
venus = Planet(mass_Venus, dist_Venus, angle=0)
earth = Planet(mass_Earth, dist_Earth, angle=0)
mars = Planet(mass_Mars, dist_Mars, angle=0)
jupiter = Planet(mass_Jupiter, dist_Jupiter, angle=0)

#the sun will be static for now, but later on we can make it move 
class Sun:
    def __init__(self, mass):
        self.mass = mass

Sun = Sun(mass_Sol)

#we will be implementing a model of the solar system using Newton's laws, the 2-body problem
#and the masses of each planet, assuming a static sun at first
def grav_force(mass, dist):
    return (grav_const*(mass*mass_Sol))/ dist**2

def centripetal_force(mass, vel, dist):
    return (mass * vel**2) / (dist)


