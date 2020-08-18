#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:56:37 2020

@author: kartasalo
"""
import numpy as np
import os
import pandas as pd
from argparse import ArgumentParser
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
parser = ArgumentParser()
# Output file.
parser.add_argument("output", type=str, help="Path to output localization file")
# Width and height of the image frame in nanometers.
parser.add_argument("width", default=22272, type=int, help="Width of the image (nm)")
parser.add_argument("height", default=22272, type=int, help="Width of the image (nm)")
# Minimum and maximum number of particles per image.
parser.add_argument("particles_min", default=100, type=int, help="Minimum number of particles")
parser.add_argument("particles_max", default=100, type=int, help="Maximum number of particles")
# Particle diameter mean and std.
parser.add_argument("diameter_mean", default=100, type=float, help="Particle diameter (nm), mean")
parser.add_argument("diameter_std", default=0, type=float, help="Particle diameter (nm), std")
# Density of localizations within particles, mean and std.
# Specified as localizations per nm^3 of particle volume.
parser.add_argument("density_mean", default=6.1115498e-4, type=float, help="Density of localizations (per nm^3), mean")
parser.add_argument("density_std", default=0, type=float, help="Density of localizations (per nm^3), std")
# Amount of "shot noise" as the number of random localizations.
parser.add_argument("noise_min", default=1000, type=int, help="Minimum number of noise events")
parser.add_argument("noise_max", default=1000, type=int, help="Maximum number of noise events")
# Visualize or not.
parser.add_argument("--visualize", action="store_true", help="Visualize generated data")
args = parser.parse_args()

# Collect parameters.
output = args.output
frame_w = args.width
frame_h = args.height
n_particles_min = args.particles_min
n_particles_max = args.particles_max
d_particles_mean = args.diameter_mean
d_particles_std = args.diameter_std
localization_density_mean = args.density_mean
localization_density_std = args.density_std
noise_shots_min = args.noise_min
noise_shots_max = args.noise_max
visualize = args.visualize

# # This is just for interactive prototyping.
#     output = "/home/kartasalo/storm-simulation.csv"
#     frame_w = 22272
#     frame_h = 22272
#     n_particles_min = 100
#     n_particles_max = 100
#     d_particles_mean = 100
#     d_particles_std = 0
#     localization_density_mean = 6.1115498e-4
#     localization_density_std = 0
#     noise_shots_min = 10000
#     noise_shots_max = 10000
#     visualize = True

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
# Initialize array of particles (id,x,y,diameter,density), one particle per row.
list_particles = np.empty((0,5),dtype=np.float64)

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
        dists = np.sqrt(np.sum((list_particles[:,1:3] - [y_center,x_center])**2,axis=1))

        # If all existing particles are further away than the diameter, accept.
        if all(dists > d):
            list_particles = np.vstack((list_particles,[particle+1,y_center,x_center,d,dens]))
            break

###################### Generate localizations #################################
list_localizations = np.empty((0,4),dtype=np.float64)

loc_id = 1
# Go through particles, one by one.
for particle in range(n_particles):
    # Pick the previously sampled data for this particle (id,x,y,diameter,density).
    particle_id = list_particles[particle,0]
    x_center = list_particles[particle,2]
    y_center = list_particles[particle,1]
    d = list_particles[particle,3]
    r = d/2
    dens = list_particles[particle,4]
    
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
                list_localizations = np.vstack((list_localizations,[loc_id,y,x,particle_id]))
                loc_id += 1
                break

###################### Generate noise #################################
for shot in range(noise_shots):
    x = np.random.uniform(0,frame_w)
    y = np.random.uniform(0,frame_h)
    list_localizations = np.vstack((list_localizations,[loc_id,y,x,0]))
    loc_id += 1

###################### Store output ##########################################
# Create output folder if it does not exist.
if not os.path.exists(os.path.dirname(output)):
    os.makedirs(os.path.dirname(output))

# Save localizations as CSV.
df = pd.DataFrame(list_localizations,columns=['id','y [nm]','x [nm]','particle id'])
df.to_csv(output.replace(".csv","_localizations.csv"), index=False)

# Save the true particle parameters as CSV.
df = pd.DataFrame(list_particles,columns=['particle id','y [nm]','x [nm]','diameter [nm]','density [per nm^3]'])
df.to_csv(output.replace(".csv","_particles.csv"), index=False)

# Plot generated data.
if visualize:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.scatter(list_localizations[:,2],list_localizations[:,1],s=1,marker=".")
    plt.xlim(0,frame_w)
    plt.ylim(0,frame_h)
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('X (nm)')
    plt.ylabel('Y (nm)')
    plt.show()



















