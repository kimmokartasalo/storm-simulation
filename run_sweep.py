#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:16:16 2020

@author: kartasalo
"""
import os
import time
import simulate_images as sim

# Constant parameters.
width = 22272
height = 22272
visualize = False

# Where to output.
outputpath = "/home/kartasalo/storm-simulation/"

# How many images to generate per parameter combination.
images_per_condition = 10

# Parameter values to sweep through.
particles_min_range = [100]
particles_max_range = [100]
diameter_mean_range = [100]
diameter_std_range = [5]
density_mean_range = [1.52788745e-4, 6.1115498e-4]
density_std_range = [0]
noise_min_range = [5000]
noise_max_range = [5000]

for particles_min in particles_min_range:
    for particles_max in particles_max_range:
        for diameter_mean in diameter_mean_range:
            for diameter_std in diameter_std_range:
                for density_mean in density_mean_range:
                    for density_std in density_std_range:
                        for noise_min in noise_min_range:
                            for noise_max in noise_max_range:
                                for im in range(images_per_condition):
                                    # Create folder name.
                                    folder = ('partmin_'+str(particles_min)+
                                              '_partmax_'+str(particles_max)+
                                              '_diamean_'+str(diameter_mean)+
                                              '_diastd_'+str(diameter_std)+
                                              '_densmean_'+str(density_mean)+
                                              '_densstd_'+str(density_std)+
                                              '_noisemin_'+str(noise_min)+
                                              '_noisemax_'+str(noise_max))
                                    
                                    # Create filename.
                                    output = os.path.join(outputpath,
                                                          folder,
                                                          str(im)+'.csv')
                                    
                                    # Count the execution time.
                                    start = time.time()
                                    print("Generating image "+output)                                    
                                    
                                    # Generate the image.
                                    sim.run_simulation(output,
                                                       width,
                                                       height, 
                                                       particles_min,
                                                       particles_max, 
                                                       diameter_mean, 
                                                       diameter_std,
                                                       density_mean, 
                                                       density_std, 
                                                       noise_min,
                                                       noise_max,
                                                       visualize)
                                    
                                    # Report execution time.
                                    end = time.time()
                                    print("Finished in "+str(end-start)+" seconds")
