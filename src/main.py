import data_validator
import delay_embedder
import persistence_analyzer
import visualizer

# Define function to get validated dimension and lag parameters from user
def get_dimension_and_lag(input_func=input):
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
   
    # User input for file paths
    file1_path = input("Enter path to first data file:")
    file2_path = input("Enter path to second data file:")

    # Get user-provided dimension and lag parameters
    dimension, lag = get_dimension_and_lag()

    # Validate the files
    validator = data_validator.Validation(file1_path, file2_path)
    if not validator.validate_files():
        print("Invalid files")
        return

    # Generate time lag embedding for both timeseries
    timeseries1 = []  # Placeholder for loaded timeseries data
    timeseries2 = []  # Placeholder for loaded timeseries data
    embedding1 = delay_embedder.DelayEmbedding(timeseries1, dimension, lag).generate_embedding()
    embedding2 = delay_embedder.DelayEmbedding(timeseries2, dimension, lag).generate_embedding()

    # Generate persistence homology and compare
    persistence_analysis = persistence_analyzer.PersistenceAnalysis(embedding1, embedding2)
    wasserstein_dist, bottleneck_dist = persistence_analysis.compare_persistence_data()

    # Visualization
    visualization = visualizer.Visualization()
    visualization.plot_point_cloud(embedding1)
    visualization.plot_point_cloud(embedding2)
    visualization.plot_persistence_homology(persistence_analysis.diagrams1)
    visualization.plot_persistence_homology(persistence_analysis.diagrams2)
    visualization.plot_distances(wasserstein_dist, bottleneck_dist)

if __name__ == "__main__":
    main()
