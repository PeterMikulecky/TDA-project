import unittest
import numpy as np
import sys
import os
from gtda.time_series import SingleTakensEmbedding

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from delay_embedder import DelayEmbedding

class TestDelayEmbedding(unittest.TestCase):
    def setUp(self):
        # Sample time series data for testing
        self.timeseries = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15])
        self.dimension = 2
        self.lag = 2
        self.emb = DelayEmbedding(self.timeseries, self.dimension, self.lag)

    def test_generate_embedding_shape(self):
        # Test if the generated embedding has the correct shape--this property has proved crucial!
        embedding = self.emb.generate_embedding()
        expected_shape = (len(self.timeseries) - (self.dimension - 1) * self.lag, self.dimension)
        self.assertEqual(embedding.shape, expected_shape, "The embedding shape is incorrect")

    def test_generate_embedding_not_none(self):
        # Test if the generated embedding is not None--would be None if embedding entirely failed
        embedding = self.emb.generate_embedding()
        self.assertIsNotNone(embedding, "The embedding should not be None")

    def test_generate_embedding_correct_values(self):
        # Test if the embedding is generated with correct values for a simple case--assuming dim=2, lag=1
        simple_timeseries = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        simple_emb = DelayEmbedding(simple_timeseries, 2, 1)
        embedding = simple_emb.generate_embedding()
        expected_embedding = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16]])
        np.testing.assert_array_equal(embedding, expected_embedding, "The embedding values are incorrect")

if __name__ == '__main__':
    unittest.main()
