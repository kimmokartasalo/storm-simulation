#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:56:37 2020

@author: kartasalo
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Function for getting number of localizations for a particle.
def localizations_per_particle(d_particle, localization_density):
    # Assuming particles are spherical, calculate surface area and volume.
    r = d_particle/2
    #area = 4*np.pi*r**2
    volume = (4/3)*np.pi*r**3
    # Number of localizations based on volume and requested density.
    localizations = round(volume*localization_density)
    
    return localizations

###################### Set parameters ########################################

# Width and height of the image frame in nanometers.
frame_w = 22272
frame_h = 22272

# Minimum and maximum number of particles per image.
n_particles_min = 100
n_particles_max = 100

# Particle diameter mean and std.
d_particles_mean = 100
d_particles_std = 0

# Density of localizations within particles, mean and std.
# Specified as localizations per nm^3 of particle volume.
localization_density_mean = 6.1115498e-4
localization_density_std = 0

# Amount of "shot noise" as the number of random localizations.
noise_shots_min = 10000
noise_shots_max = 10000

###################### Sample parameters for this image ######################
# Number of particles.
if n_particles_max != n_particles_min:
    n_particles = np.random.randint(n_particles_min,n_particles_max)
else:
    n_particles = n_particles_min

# Number of noise shots.
if noise_shots_max != noise_shots_min:
    noise_shots = np.random.randint(noise_shots_min,noise_shots_max)
else:
    noise_shots = noise_shots_min

###################### Generate particles ####################################
# Initialize array of particles (x,y,diameter,density), one particle per row.
list_particles = np.empty((0,4),dtype=np.float64)

# Go through particles, one by one.
for particle in range(n_particles):
    # Sample the diameter for this particle.
    d = np.random.normal(d_particles_mean, d_particles_std)
    
    # Sample the localization density for this particle.
    dens = np.random.normal(localization_density_mean, localization_density_std)
    
    # Sample the center of this particle randomly until non-overlapping 
    # location is found.
    while True:
        # Get a center coordinate for this particle.
        x_center = np.random.uniform(0,frame_w)
        y_center = np.random.uniform(0,frame_h)
        
        # Calculate Euclidean distance to all existing particle centers.
        dists = np.sqrt(np.sum((list_particles[:,0:2] - [y_center,x_center])**2,axis=1))

        # If all existing particles are further away than the diameter, accept.
        if all(dists > d):
            list_particles = np.vstack((list_particles,[y_center,x_center,d,dens]))
            break

###################### Generate localizations #################################
list_localizations = np.empty((0,3),dtype=np.float64)

# Go through particles, one by one.
for particle in range(n_particles):
    # Pick the previously sampled data for this particle (x,y,diameter,density).
    x_center = list_particles[particle,1]
    y_center = list_particles[particle,0]
    d = list_particles[particle,2]
    r = d/2
    dens = list_particles[particle,3]
    
    # Calculate number of localizations this particle should contain.
    n_localizations = localizations_per_particle(d, dens)
    
    # Go through localizations, one by one.
    for localization in range(n_localizations):
        # Sample a random location within the particle's x and y limits, and
        # within the image boundaries.
        while True:
            x = np.random.uniform(np.max((0,x_center-r)), np.min((frame_w,x_center+r)))
            y = np.random.uniform(np.max((0,y_center-r)), np.min((frame_h,y_center+r)))
            # If the Euclidean distance to the center of the particle is less 
            # than the particle radius, accept the point.
            if np.sqrt((y - y_center)**2 + (x - x_center)**2) <= r:
                list_localizations = np.vstack((list_localizations,[y,x,particle]))
                break

###################### Generate noise #################################
for shot in range(noise_shots):
    x = np.random.uniform(0,frame_w)
    y = np.random.uniform(0,frame_h)
    list_localizations = np.vstack((list_localizations,[y,x,np.nan]))

###################### Save localizations as CSV #############################

###################### Save the true parameters as CSV #######################

###################### Plot generated data ###################################
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(list_localizations[:,1],list_localizations[:,0],1)
plt.xlim(0,frame_w)
plt.ylim(0,frame_h)
ax.set_aspect('equal', adjustable='box')
plt.xlabel('X (nm)')
plt.ylabel('Y (nm)')






















