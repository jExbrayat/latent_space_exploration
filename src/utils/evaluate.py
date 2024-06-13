import numpy as np
from sklearn.metrics import mean_squared_error


def evaluate(model, X: np.ndarray, y: np.ndarray, metric=mean_squared_error) -> float:
    """Evaluate model according to given metric.
    I do not use keras .evaluate method since numerous cases of weird behavior have been seen.

    Args:
        model (_type_): Keras or sci-kit learn model with .predict method
        X (np.ndarray): Dataset
        y (np.ndarray): Target value
        metric (function, optional): sklearn.metrics function
        or any metric function with y_pred and y_true arguments returning a single float.
        Defaults to mean_squared_error.

    Returns:
        float: Score
    """
    # Predict dataset
    y_pred = model.predict(X)

    # Ravel data
    y = y.ravel()
    y_pred = y_pred.ravel()

    # Calculate score based on user-chosen metric
    score = metric(y_true=y, y_pred=y_pred)

    return score
