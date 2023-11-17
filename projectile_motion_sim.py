"""
Hello, and welcome to the start of my program. I will be spending some time relearning physcs, but by implementing the things I learn in python code. I might eventually switch to C++ since it's faster, but for right nwo we'll go with this

I know I'll probably need to import a bunch of stuff, but that's part of the fun

For now, I'll import numpy, scikit-learn, pandas to do the calculations and such

I'm gonna run from mechanics, to electricity and magnetism, to waves, to quantum mechanics, to general relativity, and maybe one day I'll learn to implement stuff for QED or QFT. None of that string theory shit, that's not real science.

So to begin, we have to define basic position, velocity, acceleration, and projectile motion
"""
import math

count = 100

#here we define displacement in a particular direction, based on velocity and acceleration
#the acceleration is assumed to be zero unless otherwise stated
def displacement(x_0, v_avg, t, acc=0):
    return x_0 + v_avg*t + 0.5*acc * t**2

#here we define velocity as velocity plus acceleration times time
def velocity(v_0, acc, t):
    return v_0 + acc*t

#here is another calculation of v, or v^2
#this can go into math.sqrt(v_squared) as another computation of v
def v_squared(v_0, acc, x, x_0=0):
    return v_0**2 + 2* acc*(x - x_0)

#here we will define our projectile motion function
#assuming acceleration is gravitational and we're moving in
#two directions, using theta
def projectile_motion(x_init, y_init, v_init, theta, acc=-9.8):

    #print the current state of the projectile
    print(f"x = {x_init}, y = {y_init}, velocity = {v_init}, angle = {theta*180/math.pi}°")

    dt = 0.1 #the time step will be 0.1 seconds

    v_init_x = v_init*math.cos(theta) #calculate the velocity in each direction
    v_init_y = v_init*math.sin(theta)
    
    y_step = displacement(y_init, v_init_y, dt, acc)
    x_step = displacement(x_init, v_init_x, dt)

    v_x_step = velocity(v_init_x,0,dt)
    v_y_step = velocity(v_init_y, acc, dt)

    v_step = math.sqrt(v_x_step**2 + v_y_step**2)

    theta_step = math.atan(v_y_step/v_x_step)

    if y_step >= 0:
        projectile_motion(x_step, y_step, v_step, theta_step)

    else:
        return


x_start = 0
y_start = 0
v_start = 25 #(m/s)
theta_start = math.pi/4

projectile_motion(x_start, y_start, v_start, theta_start)