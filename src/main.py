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
        for row in reader):
            file2_second_column.append(row[1])
    timeseries2 = np.array(file2_second_column)

    print("Delay-embedding timeseries 1...\n")
    embedding1 = delay_embedder.DelayEmbedding(timeseries1, dimension, lag).generate_embedding()
    print("Delay-embedding timeseries 2...\n")
    embedding2 = delay_embedder.DelayEmbedding(timeseries2, dimension, lag).generate_embedding()

    persistence_analysis = persistence_analyzer.PersistenceAnalysis(embedding1, embedding2)
    wasserstein_dist, std_lifetimes1, std_lifetimes2 = persistence_analysis.compare_persistence_data()

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
