import persim
from ripser import ripser
import numpy as np

class PersistenceAnalysis:
    """
    A class to perform persistence analysis on point cloud data embedded from timeseries.

    Attributes:
        point_cloud1 (np.ndarray): The first point cloud data.
        point_cloud2 (np.ndarray): The second point cloud data.
        diagrams1 (list or None): Persistence diagrams for the first point cloud. Initially set to None.
        diagrams2 (list or None): Persistence diagrams for the second point cloud. Initially set to None.
    """

    def __init__(self, point_cloud1, point_cloud2):
        """
        Initialize the PersistenceAnalysis class with two point clouds.

        Args:
            point_cloud1 (np.ndarray): The first point cloud data.
            point_cloud2 (np.ndarray): The second point cloud data.
        """
        self.point_cloud1 = point_cloud1
        self.point_cloud2 = point_cloud2
        self.diagrams1 = None
        self.diagrams2 = None

    def generate_persistence_homology(self, point_cloud):
        """
        Generate the persistence homology for a given point cloud.

        Args:
            point_cloud (np.ndarray): The input point cloud data.

        Returns:
            list: A list of persistence diagrams.
        """
        diagrams = ripser(point_cloud)['dgms']
        return diagrams

    def compute_wasserstein_distance(self, diagrams1, diagrams2):
        """
        Compute the Wasserstein distance between two sets of persistence diagrams.

        Args:
            diagrams1 (list): Persistence diagrams (one per homology class) from the first point cloud.
            diagrams2 (list): Persistence diagrams (one per homology class) from the second point cloud.

        Returns:
            float: The Wasserstein distance between the two sets of diagrams.
        """
        diagrams1_flat = np.vstack(diagrams1)
        diagrams2_flat = np.vstack(diagrams2)
        return persim.wasserstein(diagrams1_flat, diagrams2_flat, matching=False)

    def compute_std_lifetimes(self, diagrams):
        """
        Compute the standard deviation of lifetimes in persistence diagrams.

        Args:
            diagrams (list): A list of persistence diagrams.

        Returns:
            float: The standard deviation of lifetimes.
        """
        lifetimes = []
        for dgm in diagrams:
            if len(dgm) > 0:
                lifetime = dgm[:, 1] - dgm[:, 0]
                finite_lifetimes = lifetime[np.isfinite(lifetime)]
                lifetimes.extend(finite_lifetimes)

        if lifetimes:
            std_lifetimes = np.std(lifetimes)
        else:
            std_lifetimes = None

        return std_lifetimes
