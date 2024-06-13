import numpy as np
from keras.datasets import mnist
from keras.utils import to_categorical


def import_data(flatten: bool = False):
    """Import MNIST preprocessed data without train test split.

    Args:
        flatten (bool, optional): If true, returned MNIST images are flattened. Defaults to False.

    Returns:
        tuple: MNIST images dataset, labels, one hot encoded labels
    """
    train, test = mnist.load_data()
    X, y = np.concatenate([train[0], test[0]], axis=0), np.concatenate(
        [train[1], test[1]], axis=0
    )  # Merge train and test since we won't make actual prediction

    # Preprocess
    X = X.astype("float32") / 255
    if flatten:
        X = X.reshape(-1, 784)
    else:
        X = X.reshape(X.shape[0], 28, 28, 1)  # Reshape for encoder input shape
    y_categorical = to_categorical(y)
    return X, y, y_categorical
