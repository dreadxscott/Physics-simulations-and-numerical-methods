import pygame
import numpy as np
import math
import random
import sys

pygame.init()

(width, height) = (500, 500)

gravity = (math.pi, -0.02)
elasticity = 0.75
mass_of_air = 0.0
dampening  = .80

#creating an environment for our particles to live in
class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.color = (0,0,0)

        gravity = (math.pi, -0.02)
        elasticity = 0.75
        mass_of_air = 0.0
        dampening  = .80

    def addParticles(self,numParticles, **kwargs):
        for i in range(numParticles):
            size = kwargs.get('size', random.randint(10,20))
            radius = size
            mass = kwargs.get('mass',random.randint(100,10000))
            x = kwargs.get('x',random.uniform(size, width - radius))
            y = kwargs.get('y',random.uniform(size, height - radius))

            particle = Particle(x, y, size, radius, mass)

            particle.speed = kwargs.get('speed', random.random())
            particle.angle = kwargs.get('angle', random.random())
            particle.color = (0,0,255)
            particle.drag  = (particle.mass/(particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)
    
    def update(self):
        pass

    def display(self, particle):
        pass


class Particle:
    def __init__(self, x, y, size, radius, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.radius = radius
        self.mass = mass
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
        self.density = self.mass/(self.radius ** 2 * math.pi)
        self.color = (200 - self.density * 10, 200 - self.density * 10, 255)
        self.thickness = 2
        self.speed = 1
        self.angle = random.uniform(0, math.pi * 2)
    
    def move(self):
        self.y += self.speed*math.cos(self.angle)
        self.x += self.speed*math.sin(self.angle)

        #self.angle, self.speed = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.speed *= self.drag


    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        
    def check_collision(self, other_particle):
        distance = math.hypot(self.x - other_particle.x, self.y - other_particle.y)
        min_distance = self.radius + other_particle.radius
        return distance <= min_distance 
    
    def collide(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # Calculate relative velocity components
        rel_velocity_x = other_particle.speed * math.cos(other_particle.angle - angle) - self.speed * math.cos(self.angle - angle)
        rel_velocity_y = other_particle.speed * math.sin(other_particle.angle - angle) - self.speed * math.sin(self.angle - angle)

        # Calculate the collision response along the collision axis
        impulse = 2 * (self.mass * other_particle.mass) / (self.mass + other_particle.mass)
        impulse *= rel_velocity_x * math.cos(angle) + rel_velocity_y * math.sin(angle)

        # Update velocities
        self.speed += impulse / self.mass
        other_particle.speed -= impulse / other_particle.mass

        # Damping factor to control speed after collisions
        self.speed *= dampening  # Adjust the damping factor as needed
        other_particle.speed *= dampening 

        # Separate particles to avoid overlap
        overlap = self.radius + other_particle.radius - distance
        separation = overlap / 2
        self.x -= separation * math.cos(angle)
        self.y -= separation * math.sin(angle)
        other_particle.x += separation * math.cos(angle)
        other_particle.y += separation * math.sin(angle)

    
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1)*length1 + math.sin(angle2)*length2
    y = math.cos(angle1)*length1 + math.cos(angle2)*length2

    length = math.hypot(x,y)
    angle =  0.5 * math.pi - math.atan2(y,x)
    return angle, length

def make_particle():
    size = random.randint(10,20)
    radius = size
    density = random.randint(1, 20)
    x = random.randint(size, width - radius)
    y = random.randint(size, height - radius)

    particle = Particle(x, y, size, radius, density * size ** 2)

    particle.speed = 0

    return particle

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y -y) <= p.size:
            return p
    return None

pygame.display.set_caption('Tutorials')
background_color = (255,255,255)

screen = pygame.display.set_mode((width,height))
screen.fill(background_color)

num_particles = 10
my_particles = []

for num in range(num_particles):
    my_particles.append(make_particle())

pygame.display.flip()

running = True
selected_particle = None

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEMOTION:
            if selected_particle:
                mouseX, mouseY = pygame.mouse.get_pos()
                selected_particle.x = mouseX
                selected_particle.y = mouseY
                dx = mouseX - selected_particle.x
                dy = mouseY - selected_particle.y
                selected_particle.angle = math.atan2(dy, dx) + 0.5*math.pi
                selected_particle.speed = math.hypot(dx, dy) * 0.1
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_particle:
                mouseX, mouseY = pygame.mouse.get_pos()
                dx = mouseX - selected_particle.x
                dy = mouseY - selected_particle.y
                selected_particle.speed = math.hypot(dx, dy) * 0.10  # Adjust the multiplier for the throwing speed
                selected_particle.angle = math.atan2(dy, dx)
                selected_particle = None


    screen.fill(background_color)

    for particle in my_particles:
        if particle != selected_particle:
            particle.bounce()
            particle.move()

            #Check for collisions with other particles
            for other_particle in my_particles:
                if (particle != other_particle and particle.check_collision(other_particle)):
                    # Handle collision response using the collide function
                    particle.collide(other_particle)
        particle.display()
    
    pygame.display.flip()

    pygame.time.delay(10)  # Add a small delay to control the speed of the particles



pygame.quit()
sys.exit()