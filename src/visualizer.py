import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        pass

    def plot_point_cloud(self, point_cloud):
        # Generate plots of the point clouds
        plt.figure()
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1])
        plt.title("Point Cloud")
        plt.show()

    def plot_persistence_homology(self, persistence_data):
        # Generate persistence homology plots
        for dim, dgms in enumerate(persistence_data):
            plt.figure()
            plt.scatter(dgms[:, 0], dgms[:, 1])
            plt.title(f"Persistence Diagram (dim {dim})")
            plt.xlabel("Birth")
            plt.ylabel("Death")
            plt.show()

    def plot_distances(self, wasserstein_dist, bottleneck_dist):
        # Plot Wasserstein and Bottleneck distances
        plt.figure()
        plt.bar(["Wasserstein Distance", "Bottleneck Distance"], [wasserstein_dist, bottleneck_dist])
        plt.title("Persistence Diagram Distances")
        plt.show()
