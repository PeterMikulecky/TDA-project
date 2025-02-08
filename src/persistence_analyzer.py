import persim
from ripser import ripser

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
        return persim.wasserstein(diagrams1, diagrams2, matching=False)

    def compute_bottleneck_distance(self, diagrams1, diagrams2):
        return persim.bottleneck(diagrams1, diagrams2, matching=False)

    def compare_persistence_data(self):
        self.diagrams1 = self.generate_persistence_homology(self.point_cloud1)
        self.diagrams2 = self.generate_persistence_homology(self.point_cloud2)
        
        wasserstein_dist = self.compute_wasserstein_distance(self.diagrams1, self.diagrams2)
        bottleneck_dist = self.compute_bottleneck_distance(self.diagrams1, self.diagrams2)

        return wasserstein_dist, bottleneck_dist
