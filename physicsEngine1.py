import pygame
import numpy as np
import math
import random
import sys

pygame.init()

(width, height) = (500, 500)

gravity = (math.pi, -0.002)
drag = 0.999
elasticity = 0.75

def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1)*length1 + math.sin(angle2)*length2
    y = math.cos(angle1)*length1 + math.cos(angle2)*length2

    length = math.hypot(x,y)
    angle =  0.5 * math.pi - math.atan2(y,x)
    return angle, length

class Particle:
    def __init__(self, x,y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0,0,255)
        self.thickness = 2
        self.speed = 1
        self.angle = random.uniform(0, math.pi * 2)
    
    def move(self):
        self.y += self.speed*math.cos(self.angle)
        self.x += self.speed*math.sin(self.angle)

        self.angle, self.speed = addVectors(self.angle, self.speed, gravity[0], gravity[1])

        self.speed *= drag


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

    
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

def make_particle():
    size = random.randint(10,20)

    x = random.randint(size, width - size)
    y = random.randint(size, height - size)

    particle = Particle(x, y, size)

    particle.speed = random.random()

    return particle

pygame.display.set_caption('Tutorials')
background_color = (255,255,255)

screen = pygame.display.set_mode((width,height))
screen.fill(background_color)

num_particles = 1
my_particles = []

for num in range(num_particles):
    my_particles.append(make_particle())

pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        
    screen.fill(background_color)

    for particle in my_particles:
        particle.bounce()
        particle.move()
        particle.display()
    
    pygame.display.flip()

    pygame.time.delay(10)  # Add a small delay to control the speed of the particles



pygame.quit()
sys.exit()