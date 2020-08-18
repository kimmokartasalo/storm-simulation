# storm-simulation
Simulator for generating artificial tabular data representing STORM super-resolution microscopy images of spherical particles.

## Installation
If you are a Git user you know how to clone the repository. If not, click on the "Code" button above and download the repository as a .zip file. The code relies on Python 3.7 and a number of Python modules. The necessary Python environment can be installed using Anaconda according to the following steps:
 
1. Install Anaconda https://docs.anaconda.com/anaconda/install/.
2. Create a Conda environment based on the file conda/sthlm-simulation.yml file provided in the repo. From the command line, you can do this by running `conda env create -f conda/sthlm-simulation.yml`. Note that you need to run the command in the folder where the repository is stored. Refer to the Anaconda documentation for details.

## Usage
Before running the code, you need to always activate the Conda environment you just installed. From the command line, you can do this by running `conda activate storm-simulation`. Refer to the Anaconda documentation for details. Once the environment is active and you are in the repository folder, the actual code can be run as follows.
 
This will print a summary of how to call the code:  
`python3 simulate_images.py --help`

This is how you run the code with the desired parameters (explained below):  
`python3 simulate_images.py <output> <width> <height> <particles_min> <particles_max> <diameter_mean> <diameter_std> <density_mean> <density_std> <noise_min> <noise_max> <--visualize>`
 
For example:  
`python3 simulate_images.py "D:\somefolder\simulatedimage.csv" 22272 22272 50 100 100 10 6.11e-4 0 500 1000 --visualize`
 
## Parameters
output - The filename (including path) where output should be stored.  
width - Width of the image frame in nm.  
height - Height of the image frame in nm.  
particles_min - Minimum number of particles.  
particles_max - Maximum number of particles.  
diameter_mean - Mean diameter of particles in nm.  
diameter_std - Standard deviation of the diameter of particles in nm.  
density_mean - Mean density of localizations per particle specified as the number of localizations per cubic nm.  
density_std - Standard deviation of density of localizations per particle specified as the number of localizations per cubic nm.  
noise_min - Minimum number of noise localizations.  
noise_max - Maximum number of noise localizations.  
--visualize - If this parameter is provided (note you need the --), the output is visualized interactively.  

## Output
The code generates two CSV files as output.  
`<output>_particles.csv` - Table of all the generated particles and their true parameters.  
`<output>_localizations.csv` - Table of all the generated localizations.
  
## Running parameter sweeps
The simulator can be easily run to generate a large number of images with different parameters. The script `run_sweep.py`is meant as an example for this purpose. You can modify the parameter combinations to use and the number of images to generate for each combination by editing the script. The script can then be run interactively in e.g. Spyder or from the command line with `python3 run_sweep.py`.
 
The script will create one subdirectory in the requested output folder per parameter combination. The images representing those parameters are stored in the subdirectory and named with a running number.

## Citing
If you use the code for an article, please contact the author.
