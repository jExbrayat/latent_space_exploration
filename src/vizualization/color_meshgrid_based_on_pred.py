import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from keras.models import Model, load_model

from src.models.define_model import create_encod_decod
from src.models.split_encoder_decoder import split_encoder_decoder
from src.utils.create_mesh_grid_on_latent_space import create_meshgrid


def color_meshgrid_based_on_pred(
    autoencoder_path: str,
    classifier_path: str,
    save_path: str,
    need_to_rebuild_model: bool = False,
    flatten_data: bool = False,
) -> None:
    """Create a plot with whole meshgrid colored based on the classifier's predictions and save it.

    Args:
        autoencoder_path (str): Path referencing to the autoencoder in the repository.
        autoencoder_file_format (str): Format of the saved model. Used to constitue the model's file path.
        classifier_path (str): Path to the classifier making prediction on decoded meshgrid points' class.
        save_path (str): Path to which save the plot and the labels grid (two output files: .npy and .png)
        e.g. models/latent_space_viz/colormaps
        need_to_rebuild_model (bool): If only weights were saved, setting to True will rebuild
        the model and load the weights under .h5 file. Warning: be sure src.models.define_model package builds the right model.
    """

    # Load models
    classifier = load_model(classifier_path)
    if not need_to_rebuild_model:
        encod_decod = load_model(autoencoder_path)
    else:
        encod_decod = (
            create_encod_decod()
        )  # If model is built using keras.models Model API
        encod_decod.load_weights(autoencoder_path)

    # Split encoder and decoder
    if not need_to_rebuild_model:
        encod, decod = split_encoder_decoder(encoder_decoder_model=encod_decod)
    else:
        # Get encoder
        encod = Model(  # If using keras.models Model API
            encod_decod.layers[0].input, encod_decod.layers[1].output[0]
        )  # Get z_mean, the expectation of latent representation, as output
        # Get decoder
        decod = Model(
            encod_decod.get_layer("decoder").input,
            encod_decod.get_layer("decoder").output,
        )

    # Create meshgrid
    x_coordinates, y_coordinates = create_meshgrid(
        encod=encod, flatten_data=flatten_data
    )

    # Stack x_coordinates and y_coordinates to create a grid of data points
    # in latent space of shape (100, 100, 2)
    # (We are cautious with array manipulation here)
    data_points_grid = np.stack([x_coordinates, y_coordinates], axis=-1)

    # Reshape meshgrid like a dataset for decoder
    grid_dataset = data_points_grid.reshape(10_000, 2)

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

    # Save colormap as numpy array
    np.save(save_path, y_pred_grid)

    # Create a DataFrame to use with Seaborn
    data = pd.DataFrame(
        {
            "x": x_coordinates.ravel(),
            "y": y_coordinates.ravel(),
            "class": y_pred_grid.ravel(),
        }
    )

    # Create the scatter plot
    plt.figure(figsize=(10, 8))
    scatter = sns.scatterplot(
        x="x", y="y", hue="class", palette="tab10", data=data, legend="full"
    )

    # Customize the legend
    scatter.legend(title="Encoded digit")

    # Add title and save the plot
    plt.title(
        "Latent space areas colored based on the corresponding encoded digit image"
    )
    plt.xlabel("Latent space first dimension")
    plt.ylabel("Latent space second dimension")
    plt.savefig(save_path)
    plt.close()
