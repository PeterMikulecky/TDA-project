"""
main.py

This is the main driver script for the TDA Time Series Visualizer package.

The package offers a user-friendly way for non-specialist researchers to assess 
whether their time series data might benefit from topological data analysis (TDA).

This driver makes the app available from the CLI. For a GUI-driven interface, use
the alternative driver, TDAVisualizerApp.py.

Workflow:
1. Prompt the user to provide paths to two CSV files, each containing two columns: 
    timestep and signal data.
2. Prompt the user to input parameters for dimension and lag.
3. Validate the data in the provided files.
4. Use the dimension and lag parameters to perform delay-embedding of the time 
    series, producing point clouds.
5. Subject the point clouds to persistence homology analysis to produce persistence
    diagrams, highlighting the persistence of topological features across homology 
    groups (H0: points, H1: holes, H2: volumes).
6. Compare the persistence diagrams of the two time series by calculating the 
    Wasserstein distance, normalized against the standard deviation of the 
    persistence lifetimes of each persistence diagram.
7. Output five plots, saving them to the source code directory:
    - Point cloud for time series 1
    - Point cloud for time series 2
    - Persistence diagram for time series 1
    - Persistence diagram for time series 2
    - Wasserstein distance normalized against the lifetime standard deviation of 
        each persistence diagram

Dependencies:
- data_validator.py: Validates the data in the provided CSV files.
- delay_embedder.py: Delay-embeds the time series to produce point clouds.
- persistence_analyzer.py: Analyzes the point clouds using persistence homology 
    to produce persistence diagrams.
- visualizer.py: Visualizes the point clouds and persistence diagrams, and 
    calculates the Wasserstein distance.
- other python packages from the PSL or installable by pip, as detailed in 
    requirements.txt.

Example:
To run the script, from within /TDA-project/src/, use one of the following commands:
    python main.py
    python3 main.py

Authors:
    Peter Mikulecky and Patrick Hudson

Date:
    2/25/25

"""
# Imports
import numpy as np
import csv
import data_validator
import delay_embedder
import persistence_analyzer
import visualizer

def get_dimension_and_lag(input_func=input):
    """
    Prompt the user to enter positive integer values for dimension and lag parameters.

    Args:
        input_func (function): Function to get input from the user, implements validation.

    Returns:
        tuple: A tuple containing two positive integers (dimension, lag).
    """
    while True:
        try:
            dimension = int(input_func("Enter a positive integer dimension parameter: "))
            lag = int(input_func("Enter a positive integer lag parameter: "))
            if dimension <= 0 or lag <= 0:
                print("Both dimension and lag must be positive integers. Please try again.")
            else:
                return dimension, lag
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def main():
    """
    Main function to execute the Topological Data Analysis Visualizer application.

    Steps:
        1. Prompt users for paths to two timeseries .csv files.
        2. Get dimension and lag parameters from user.
        3. Validate the timeseries data files.
        4. Convert the second column (i.e., the signal) of each data file to numpy arrays.
        5. Perform delay embedding on the time series data.
        6. Perform persistence analysis on the embedded data.
        7. Generate visualizations and save them to the local directory.
    """
    file1_path = input("Enter path to first data file:")
    file2_path = input("Enter path to second data file:")
    dimension, lag = get_dimension_and_lag()

    print("Validating files...\n")
    validator = data_validator.Validation(file1_path, file2_path)
    if not validator.validate_files():
        print("Invalid files")
        return

    print("Converting file 1 to array...\n")
    file1_second_column = []
    with open(file1_path, 'r') as file1:
        reader = csv.reader(file1)
        next(reader)
        for row in reader:
            file1_second_column.append(row[1])
    timeseries1 = np.array(file1_second_column)

    print("Converting file 2 to array...\n")
    file2_second_column = []
    with open(file2_path, 'r') as file2:
        reader = csv.reader(file2)
        next(reader)
        for row in reader:
            file2_second_column.append(row[1])
    timeseries2 = np.array(file2_second_column)

    print("Delay-embedding timeseries 1...\n")
    embedding1 = delay_embedder.DelayEmbedding(timeseries1, dimension, lag).generate_embedding()
    print("Delay-embedding timeseries 2...\n")
    embedding2 = delay_embedder.DelayEmbedding(timeseries2, dimension, lag).generate_embedding()

    print("Calculating persistence diagrams. UserWarnings are normal and expected. This could take a few minutes...")
    persistence_analysis = persistence_analyzer.PersistenceAnalysis(embedding1, embedding2)
    persistence_analysis.diagrams1 = persistence_analysis.generate_persistence_homology(embedding1)
    persistence_analysis.diagrams2 = persistence_analysis.generate_persistence_homology(embedding2)
    
    wasserstein_dist = persistence_analysis.compute_wasserstein_distance(persistence_analysis.diagrams1, persistence_analysis.diagrams2)
    std_lifetimes1 = persistence_analysis.compute_std_lifetimes(persistence_analysis.diagrams1)
    std_lifetimes2 = persistence_analysis.compute_std_lifetimes(persistence_analysis.diagrams2)

    print("Generating plots and saving to the application's local directory...\n")
    visualization = visualizer.Visualization()
    visualization.plot_point_cloud(embedding1)
    visualization.plot_point_cloud(embedding2)
    visualization.plot_persistence_homology(persistence_analysis.diagrams1)
    visualization.plot_persistence_homology(persistence_analysis.diagrams2)
    visualization.plot_normalized_wasserstein(wasserstein_dist, std_lifetimes1, std_lifetimes2)
    print("Thanks for using the Topological Data Analysis Visualizer!")

if __name__ == "__main__":
    main()
