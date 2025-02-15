# Unit tests for persistence_analyzer class
import unittest
import numpy as np
from persistence_analyzer import PersistenceAnalysis

# Class containing unittest test cases
class TestPersistenceAnalysis(unittest.TestCase):
    # Generate randomized data for use in unit tests
    def setUp(self):
        self.point_cloud1 = np.random.random((100, 2))
        self.point_cloud2 = np.random.random((100, 2))
        self.analysis = PersistenceAnalysis(self.point_cloud1, self.point_cloud2)

    # Test persistence homology method for ability to produce output
    def test_generate_persistence_homology(self):
        diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        diagrams2 = self.analysis.generate_persistence_homology(self.point_cloud2)
        self.assertTrue(len(diagrams1) > 0)
        self.assertTrue(len(diagrams2) > 0)
        
    # Test Wasserstein distance calculator for ability to produce float output 
    def test_compute_wasserstein_distance(self):
        diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        diagrams2 = self.analysis.generate_persistence_homology(self.point_cloud2)
        wasserstein_dist = self.analysis.compute_wasserstein_distance(diagrams1, diagrams2)
        self.assertIsInstance(wasserstein_dist, float)

    # Test Bottleneck distance calculator for ability to produce float output
    def test_compute_bottleneck_distance(self):
        diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        diagrams2 = self.analysis.generate_persistence_homology(self.point_cloud2)
        bottleneck_dist = self.analysis.compute_bottleneck_distance(diagrams1, diagrams2)
        self.assertIsInstance(bottleneck_dist, float)

    # Test compare_persistence_data mathod for ability to call preceding methods
    def test_compare_persistence_data(self):
        wasserstein_dist, bottleneck_dist = self.analysis.compare_persistence_data()
        self.assertIsInstance(wasserstein_dist, float)
        self.assertIsInstance(bottleneck_dist, float)

if __name__ == "__main__":
    unittest.main()
