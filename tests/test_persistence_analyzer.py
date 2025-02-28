import numpy as np
import sys
import os
import unittest  # Make sure to import unittest

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
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
        self.assertTrue(isinstance(diagrams1, list) and len(diagrams1) > 0)
        self.assertTrue(isinstance(diagrams2, list) and len(diagrams2) > 0)

    # Test Wasserstein distance calculator for ability to produce float output
    def test_compute_wasserstein_distance(self):
        diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        diagrams2 = self.analysis.generate_persistence_homology(self.point_cloud2)
        wasserstein_dist = self.analysis.compute_wasserstein_distance(diagrams1, diagrams2)
        self.assertIsInstance(wasserstein_dist, float)

    # Test std_lifetimes distance calculator for ability to produce float output
    def test_compute_std_lifetimes(self):
        diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        std_lifetimes1 = self.analysis.compute_std_lifetimes(diagrams1)
        self.assertTrue(std_lifetimes1 is None or isinstance(std_lifetimes1, float))

    # Test compare_persistence_data method for ability to call preceding methods
    def test_compare_persistence_data(self):
        self.analysis.diagrams1 = self.analysis.generate_persistence_homology(self.point_cloud1)
        self.analysis.diagrams2 = self.analysis.generate_persistence_homology(self.point_cloud2)
        wasserstein_dist = self.analysis.compute_wasserstein_distance(self.analysis.diagrams1, self.analysis.diagrams2)
        std_lifetimes1 = self.analysis.compute_std_lifetimes(self.analysis.diagrams1)
        std_lifetimes2 = self.analysis.compute_std_lifetimes(self.analysis.diagrams2)
        print("Wasserstein Distance:", wasserstein_dist)
        print("Std Lifetimes 1:", std_lifetimes1)
        print("Std Lifetimes 2:", std_lifetimes2)
        self.assertIsInstance(wasserstein_dist, float)
        self.assertTrue(std_lifetimes1 is None or isinstance(std_lifetimes1, float))
        self.assertTrue(std_lifetimes2 is None or isinstance(std_lifetimes2, float))

if __name__ == "__main__":
    unittest.main()
