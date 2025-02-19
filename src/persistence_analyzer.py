import persim
from ripser import ripser
import numpy as np

class PersistenceAnalysis:
    def __init__(self, point_cloud1, point_cloud2):
        self.point_cloud1 = point_cloud1
        self.point_cloud2 = point_cloud2
        self.diagrams1 = None
        self.diagrams2 = None

    def generate_persistence_homology(self, point_cloud):
        diagrams = ripser(point_cloud)['dgms']
        return diagrams

    def compute_wasserstein_distance(self, diagrams1, diagrams2):
        # Flatten diagrams for input into persim
        diagrams1_flat = np.vstack(diagrams1)
        diagrams2_flat = np.vstack(diagrams2)
        return persim.wasserstein(diagrams1_flat, diagrams2_flat, matching=False)

    def compute_bottleneck_distance(self, diagrams1, diagrams2):
        # Flatten diagrams for input into persim
        diagrams1_flat = np.vstack(diagrams1)
        diagrams2_flat = np.vstack(diagrams2)
        return persim.bottleneck(diagrams1_flat, diagrams2_flat, matching=False)

    def compare_persistence_data(self):
        print("Working on persistence diagram for timeseries 1...\n")
        self.diagrams1 = self.generate_persistence_homology(self.point_cloud1)
        print("Working on persistence diagram for timeseries 2...\n")
        self.diagrams2 = self.generate_persistence_homology(self.point_cloud2)
        print("Calculating Wasserstein distance. UserWarnings are expected. This could take a few minutes...\n")
        wasserstein_dist = self.compute_wasserstein_distance(self.diagrams1, self.diagrams2)
        print("Calculating Bottleneck distance. UserWarnings are expected. This could take a few minutes...\n")
        bottleneck_dist = self.compute_bottleneck_distance(self.diagrams1, self.diagrams2)

        return wasserstein_dist, bottleneck_dist
