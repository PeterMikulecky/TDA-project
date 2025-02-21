# CAS502 PROJECT

## Title:
Topological Data Analysis Visualizer

## Description:
This project develops a user-friendly tool for non-experts who want to assess
whether their time series data could benefit from persistence homology analysis. 
The tool prompts the user to upload two sets of time series data (intended for 
comparison), validates the data, prompts the user for a few parameters, and then 
subjects the validated data to a three-phase pipeline.

The first phase embeds the time series data into point clouds. The second 
extracts persistence homology profiles from the point clouds. The third 
calculates a distance metric to assess the topological similarites of the two 
datasets. The tool outputs plots of the point clouds, persistence homololgy 
visualizations and the final distance metric.

## Team Members:
Peter Mikulecky and Patrick Hudson

## Bugs, Feature Requests and Contribution:
Please direct all such correspondence to pmikule1@asu.edu.

## User Documentation:

### Installation:
The application runs as a Python module which can be accessed by cloning this 
repository. Python 3.12.3 was the devlopment environment. See INSTALL.md for 
instructions on cloning the repository, setting up and activating a virtual 
environment, installing dependencies and running the application.

### User-provided time series data:
The application prompts the user for paths to two time series data files that 
will undergo TDA analysis for comparison. **Each file should be in two-column** 
**.csv format.** The first column should contain time dimension data, and the 
second column should contain the signal dimension data. Columns may contain a 
single header row.

The application is currently configured to impose a maximum length of 10,000 
rows for each time series. This configuration can be adjusted within the 
data_validator.py class file, but was selected for reasonable run times on modern 
laptop processors.

The most useful results will be obtained for time series of similar length, 
comparing data collected under similar conditions but which may reflect 
significantly different dynamics.

### Dimension and Lag parameters:
The application prompts the user to enter integer arguments for dimension and lag
parameters. These parameters control the implmentation of delay-embedding of the 
time series to produce point clouds. For most datasets, it is reasonable to start 
with dimension 2 or 3. 

The lag parameter is sensitive to the properties of the time series. Empirically, 
the best results are often achieved when the lag is set to about 1.5x the number 
of time points contained within one cycle of the most prominent periodic feature 
of the time series. For example, if the data are sampled at 1 observation per 
minute, and the major periodicity occurs once per 10 minutes, then a lag of 15 is
a good place to start.

### Processing time and runtime messages
The application displays updates as it moves through each step of the TDA 
processing pipeline. Most steps occur very rapidly. **Calculating the Wasserstein** 
**distance** (a measure of the difference between the two persistence diagrams)
**can take much longer, up to several minutes** depending on the length of the 
time series. 

During the calculation of the Wasserstein distance, **it is normal and expected** 
**to observe "UserWarning" messages about the existence of infinities within the** 
**data points**. Such points are a feature of essentially all persistence 
diagrams (in the H0 homology class), and the Wasserstein algorithm gracefully 
handles these UserWarnings.

### Output files:
The application generates five plot files per run. The plot files are in .png 
format and are automatically saved to the same /TDA-project/src/ directory that 
contains the main.py script.

#### *Point clouds*
Two files represent 2D visualizations of the point clouds for each time series. 
When the dimension parameter selected for delay-embedding is higher than 2, 
these plots represent 2D projections of the higher-dimensional embedding. 

#### *Persistence homology ("birth-death") diagrams*
Two of the files represent persistence homology digrams for each of the time 
series. The plots combine H0 and H1 homology classes ("points" and "holes"), 
color-coding them for clarity. In most cases, interesting differences between 
timeseries occur in the H1 class, where the off-diagonal lifetimes of H1 
features may differ. 

#### *Normalized Wasserstein distance plot*
One file is a bar chart comparing the normalized Wasserstein distances 
calculated from the persistence homology diagrams. The Wasserstein distance is 
a non-Euclidean metric capturing the magnitude of difference between the two 
persistence homology diagrams. Intuitively, the larger the Wasserstein distance, 
the more "work" is required to transform one persistence homology diagram into 
the other. The bar chart normalizes this Wasserstein distance against the 
standard deviation of persistence lifetimes observed in each diagram. This 
allows one compare inter-diagram distance against intra-diagram variability.
