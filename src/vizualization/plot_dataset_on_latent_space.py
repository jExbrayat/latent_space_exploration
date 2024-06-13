from keras.models import Model
import re
from os import listdir

from src.data.import_data import import_data
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model, Model
from src.models.define_model import create_encod_decod
from src.models.split_encoder_decoder import split_encoder_decoder

# TODO: write whole code as functions


def plot_mnist_on_latent_space(
    model_path: str, save_path: str, display: bool = False, flatten_data: bool = False
):
    """Generate plot of all MNIST images representation on latent space.
    This function aims to make a visualization of an autoencoder latent space.

    Args:
        model_path (str): Path to autoencoder model
        save_path (str): Path to save plot image
        display (bool): Set to true to display the figure. Default to False.
    """
    # Import tools
    X, _, _ = import_data(flatten=flatten_data)
    encod_decod = load_model(model_path)
    encod, _ = split_encoder_decoder(encod_decod)

    # Encode dataset
    X_encod = encod.predict(X)

    # Scatter plot data points on latent space
    plt.scatter(X_encod[:, 0], X_encod[:, 1])
    plt.title("Projection of actual MNIST images on latent space")
    plt.xlabel("First dimension")
    plt.ylabel("Second dimension")
    plt.savefig(save_path)
    if display:
        plt.show()
    plt.close()


# Define a custom sorting function to extract the epoch number from the filename
def extract_epoch(filename):
    return int(re.search(r"\d+", filename).group())


# Get model filenames sorted by epoch
filenames = sorted(
    listdir("models/checkpoints/encod_decod_ConvDense-5"), key=extract_epoch
)

# Iterate over all checkpoints of ConvDense-5
for model_filename in filenames:
    # Define model path
    model_path = f"models/checkpoints/encod_decod_ConvDense-5/{model_filename}"
    # Define save path
    save_path = f"models/latent_space_viz/actual_data_scatter_plot/ConvDense-5_through_epochs/{model_filename[:-6]}"  # Remove .keras part of the filename
    # Plot and save
    plot_mnist_on_latent_space(model_path=model_path, save_path=save_path)


#  For Keras Model API

# Define trained classifier path
classifier_path = "models/classifiers/classifier.keras"
classifier = load_model(classifier_path)

# Determine lower and upper bounds of the two axes (second dimension of array)
dim1_lower_bound = 0
dim2_lower_bound = 0
dim1_upper_bound = 1
dim2_upper_bound = 1

# Make meshgrid on the two dimensional latent space
n_points_dim1, n_points_dim2 = 100, 100
dim1_points = np.linspace(dim1_lower_bound, dim1_upper_bound, n_points_dim1)
dim2_points = np.linspace(dim2_lower_bound, dim2_upper_bound, n_points_dim2)
grid = np.meshgrid(dim1_points, dim2_points)
x_coordinates, y_coordinates = grid[0], grid[1]

# Stack x_coordinates and y_coordinates to create a grid of data points
# in latent space of shape (100, 100, 2)
# (We are cautious with array manipulation here)
data_points_grid = np.stack([x_coordinates, y_coordinates], axis=-1)

# Reshape meshgrid like a dataset for decoder
grid_dataset = data_points_grid.reshape(10_000, 2)

# Define name of model for the desired latent space
autoencoder_name = "VAE-1"

# Define save path
save_path = f"models/latent_space_viz/colormaps/{autoencoder_name}_through_epochs"

# Get list of checkpoints
checkpoints_path = "models/checkpoints/encod_decod_VAE-1"
checkpoints = listdir(checkpoints_path)

for autoencoder_ckpoint in checkpoints[:2]:
    # Define autoencoder path
    autoencoder_path = f"{checkpoints_path}/{autoencoder_ckpoint}"

    encod_decod = create_encod_decod()  # If model is built using keras.models Model API
    encod_decod.load_weights(autoencoder_path)

    # Split encoder and decoder
    encod = Model(  # If using keras.models Model API
        encod_decod.layers[0].input, encod_decod.layers[1].output[0]
    )  # Get z_mean, the expectation of latent representation, as output

    # Get encoder
    decod = Model(
        encod_decod.get_layer("decoder").input, encod_decod.get_layer("decoder").output
    )

    # Decod meshgrid
    decoded_grid = decod.predict(grid_dataset)

    # Reshape decoded images to classifier input shape
    decoded_grid_reshape = decoded_grid.reshape(10_000, 28, 28, 1)

    # Predict class for each decoded image of meshgrid
    y_pred = classifier.predict(decoded_grid_reshape)

    # Convert one hot encoding to categorical integer variable
    y_pred_categorical = np.argmax(y_pred, axis=1)

    # Reshape predictions like an actual grid
    y_pred_grid = y_pred_categorical.reshape(100, 100)

    # Color grid based on prediction
    plt.scatter(x_coordinates, y_coordinates, c=y_pred_grid)
    plt.savefig(f"{save_path}/{autoencoder_ckpoint[:-3]}")
    plt.close()
