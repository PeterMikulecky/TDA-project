import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        self.point_cloud_counter = 0  # Counter for point cloud plots
        self.persistence_homology_counter = 0  # Counter for persistence homology plots

    def plot_point_cloud(self, point_cloud):
        # Generate plots of the point clouds
        plt.figure()
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1])
        plt.title("Point Cloud")
        
        # Generate a unique file name
        filename = f'point_cloud_{self.point_cloud_counter}.png'
        plt.savefig(filename)  # Save the plot as an image file
        plt.close()  # Close the figure
        
        self.point_cloud_counter += 1  # Increment the counter

    def plot_persistence_homology(self, persistence_data):
        # Generate persistence homology plots
        for dim, dgms in enumerate(persistence_data):
            plt.figure()
            plt.scatter(dgms[:, 0], dgms[:, 1])
            plt.title(f"Persistence Diagram (dim {dim})")
            plt.xlabel("Birth")
            plt.ylabel("Death")

            # Generate a unique file name for each diagram
            filename = f'persistence_diagram_dim_{dim}_{self.persistence_homology_counter}.png'
            plt.savefig(filename)  # Save the plot as an image file
            plt.close()  # Close the figure
            
            self.persistence_homology_counter += 1  # Increment the counter

    def plot_distances(self, wasserstein_dist, bottleneck_dist):
        # Plot Wasserstein and Bottleneck distances
        plt.figure()
        plt.bar(["Wasserstein Distance", "Bottleneck Distance"], [wasserstein_dist, bottleneck_dist])
        plt.title("Persistence Diagram Distances")
        plt.savefig('distances.png')  # Save the plot as an image file
        plt.close()  # Close the figure
