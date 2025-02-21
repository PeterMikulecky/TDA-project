import matplotlib.pyplot as plt

class Visualization:
    """
    A class to generate plots for point clouds, persistence homology, and normalized Wasserstein distance.

    Attributes:
        point_cloud_counter (int): Counter for naming point cloud plot files.
        persistence_homology_counter (int): Counter for naming persistence homology plot files.
    """

    def __init__(self):
        """
        Initialize the Visualization class with counters for plot files.
        """
        self.point_cloud_counter = 0
        self.persistence_homology_counter = 0

    def plot_point_cloud(self, point_cloud):
        """
        Plot and save a scatter plot of a point cloud.

        Args:
            point_cloud (np.ndarray): The point cloud data to be plotted.
        """
        plt.figure()
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1])
        plt.title("Point Cloud")
        filename = f'point_cloud_{self.point_cloud_counter}.png'
        plt.savefig(filename)
        plt.close()
        self.point_cloud_counter += 1

    def plot_persistence_homology(self, persistence_data):
        """
        Plot and save a persistence diagram for homology groups H0 and H1.

        Args:
            persistence_data (list): Persistence diagrams for different homology dimensions.
        """
        plt.figure()
        colors = ['b', 'r']
        labels = ['H0', 'H1']

        for dim, dgms in enumerate(persistence_data):
            plt.scatter(dgms[:, 0], dgms[:, 1], c=colors[dim], label=labels[dim])

        plt.title("Persistence Diagram (H0 and H1)")
        plt.xlabel("Birth")
        plt.ylabel("Death")
        plt.legend()
        filename = f'persistence_diagram_combined_{self.persistence_homology_counter}.png'
        plt.savefig(filename)
        plt.close()
        self.persistence_homology_counter += 1

    def plot_normalized_wasserstein(self, wasserstein_dist, std_lifetimes1, std_lifetimes2):
        """
        Plot and save a bar chart of the normalized Wasserstein distance for two persistence diagrams.

        Args:
            wasserstein_dist (float): The Wasserstein distance between two persistence diagrams.
            std_lifetimes1 (float): The standard deviation of lifetimes for the first persistence diagram.
            std_lifetimes2 (float): The standard deviation of lifetimes for the second persistence diagram.
        """
        print("Wasserstein Distance:", wasserstein_dist)
        print("Standard Deviation of Lifetimes for Time Series 1:", std_lifetimes1)
        print("Standard Deviation of Lifetimes for Time Series 2:", std_lifetimes2)

        normalized_wasserstein1 = wasserstein_dist / std_lifetimes1
        normalized_wasserstein2 = wasserstein_dist / std_lifetimes2

        plt.figure()
        values = [normalized_wasserstein1, normalized_wasserstein2]
        labels = ["Normalized Wasserstein (TS1)", "Normalized Wasserstein (TS2)"]
        colors = ['b', 'g']

        plt.bar(labels, values, color=colors)
        plt.title("Normalized Wasserstein Distance")
        plt.ylabel("Normalized Distance")
        plt.savefig('normalized_wasserstein.png')
        plt.close()
