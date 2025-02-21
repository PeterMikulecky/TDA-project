import numpy as np
from sklearn.neighbors import KDTree
from ripser import ripser
from gtda.time_series import SingleTakensEmbedding

class DelayEmbedding:
    """
    A class to perform delay embedding on user-provided timeseries data.

    Attributes:
        timeseries (array-like): The input time series data.
        dimension (int): The embedding dimension.
        lag (int): The lag parameter for embedding.
        embeddings (np.ndarray or None): The generated embeddings. Initially set to None.
    """

    def __init__(self, timeseries, dimension, lag):
        """
        Initialize the DelayEmbedding class with the given time series, dimension, and lag.

        Args:
            timeseries (array-like): The input time series data.
            dimension (int): The embedding dimension.
            lag (int): The lag parameter for embedding.
        """
        self.timeseries = timeseries
        self.dimension = dimension
        self.lag = lag
        self.embeddings = None

    def generate_embedding(self):
        """
        Generate the delay embedding for the timeseries data.

        Returns:
            np.ndarray: The generated embeddings.
        """
        self.timeseries = np.array(self.timeseries)  # Convert timeseries to a NumPy array
        embedding = SingleTakensEmbedding(parameters_type='fixed', time_delay=self.lag, dimension=self.dimension)
        self.embeddings = embedding.fit_transform(self.timeseries.reshape(-1, 1))
        return self.embeddings

    def verify_embedding(self):
        """
        Verify the quality of the generated embedding (not implmented yet).

        This method is intended to verify the quality of the embedding by using K-nearest-neighbors.
        """
        pass
