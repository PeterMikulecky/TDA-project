# CAS502 PROJECT

## Title: 
Topological Data Analysis Visualizer

## Description:
This project develops a user-friendly tool for non-experts who want to assess whether their
time series data could benefit from persistence homology analysis. The tool prompts the user
to upload two sets of time series data (intended for comparison), validates the data, prompts
the user for a few parameters, and then subjects the validated data to a three-phase pipeline.
The first phase embeds the time series data into point clouds. The second extracts persistence
homology profiles from the point clouds. The third calculates a distance metric to assess the
topological similarites of the two datasets. The tool outputs plots of the point clouds, 
persistence homololgy visualizations and the final distance metric.

## Team Members:
Peter Mikulecky and Patrick Hudson 

## Anticipated Challenges
We think that the primary challenge will be determining default parameters for the TDA pipeline
that produce useful results for the broadest range of data domains. TDA results are sufficiently
sensitive to parameter selection that it may prove difficult to find a "sweet spot" that
produces informative results on the first pass for non-technical users. Automating parameter
selection based on a grid search of results with the user-provided data is a reasonable remedy,
but the calculations could prove time-consuming for larger datasets. We have therefore added an
automated parameter selection feature as nice-to-have. Another, more straightforward but still
potentially challenging problem is configuring plots to scale properly based on results. Finally,
the list of criteria we will need to include for data validation is fairly long, so we believe
it will take some time to get validation to function reliably.
