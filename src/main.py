import data_validator
import delay_embedder
import persistence_analyzer
import visualizer

def main():
   
    # User input for file paths
    file1_path = input("Enter path to first data file:")
    file2_path = input("Enter path to second data file:")

    # User input for dimension and lag parameters
    dimension = int(input("Enter an integer dimension parameter: "))
    lag = int(input("Enter an integer lag parameter: "))

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
