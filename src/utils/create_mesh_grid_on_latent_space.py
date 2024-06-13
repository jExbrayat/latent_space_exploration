import numpy as np

from src.data.import_data import import_data


def create_meshgrid(encod, flatten_data: bool = False) -> tuple:
    """Create a 2 dimensional meshgrid of shape (100, 100) bounded by
    the extrema of the representations of encoded MNIST images in latent space.
    Meshgrid will serve to interactively visualize latent space thanks to decoded images on each point of it.

    Args:
        encod: Keras model. Encoding part of the autoencoder.
        flatten_data (bool, optional): Set to True if autoencoder input shape is (784,). Defaults to False.

    Returns:
        tuple: (x coordinates of numpy meshgrid, y coordinates of numpy meshgrid)
    """
    # Load data to encode
    X, _, _ = import_data(flatten=flatten_data)

    # Encod the whole dataset
    X_encod = encod.predict(X)

    X_encod.shape  # X_encod shape is (60_000, 2)

    # Determine lower and upper bounds of the two axes (second dimension of array)
    dim1_lower_bound = np.min(X_encod[:, 0])
    dim2_lower_bound = np.min(X_encod[:, 1])
    dim1_upper_bound = np.max(X_encod[:, 0])
    dim2_upper_bound = np.max(X_encod[:, 1])

    # Make meshgrid on the two dimensional latent space
    n_points_dim1, n_points_dim2 = 100, 100
    dim1_points = np.linspace(dim1_lower_bound, dim1_upper_bound, n_points_dim1)
    dim2_points = np.linspace(dim2_lower_bound, dim2_upper_bound, n_points_dim2)
    grid = np.meshgrid(dim1_points, dim2_points)
    x_coordinates, y_coordinates = grid[0], grid[1]

    return x_coordinates, y_coordinates
