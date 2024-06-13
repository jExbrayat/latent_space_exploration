import pickle

from keras.models import load_model

from src.data.import_data import import_data
from src.utils.evaluate import evaluate


def evaluate_autoencoder(
    autoencoder_path: str,
    saving_label: str,
    save_path: str,
    data_format: str = "default",
):
    """Evaluate autoencoder and save its score in a dictionnary

    Args:
        autoencoder_path (str): Path of autoencoder to evaluate
        saving_label (str): Desired dictionnary key for saved score
        data_format (str, optional): "flatten" if autoencoder input layer requires it. Defaults to "default".
    """

    # Open former results dictionnary
    try:
        with open(f"{save_path}.pkl", "rb") as f:
            models_eval = pickle.load(f)
    except:
        print(f"A dictionnary is created at {save_path}")
        models_eval = {}

    # Import model to evaluate
    encod_decod = load_model(autoencoder_path)

    # Import data
    flatten = data_format == "flatten"
    X, _, _ = import_data(flatten=flatten)

    # Evaluate model
    mse = evaluate(encod_decod, X=X, y=X)

    # Save model score in dictionnary
    models_eval[saving_label] = mse
    with open(f"{save_path}.pkl", "wb") as f:
        pickle.dump(models_eval, f)


save_path = "models/models_comparison/autoencoders_score"
if __name__ == "__main__":

    evaluate_autoencoder(
        "models/autoencoders/encod_decod_ConvDense-5.keras",
        "ConvDense-5",
        save_path=save_path,
    )
