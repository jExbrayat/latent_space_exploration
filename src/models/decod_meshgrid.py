import matplotlib.pyplot as plt
import numpy as np
from keras.models import Model, load_model

from src.models.define_model import create_encod_decod
from src.models.split_encoder_decoder import split_encoder_decoder
from src.utils.create_mesh_grid_on_latent_space import create_meshgrid

# Define autoencoder name
autoencoder_name = "VAE-1"

# Define file format
model_format = ".h5"

# Load complete encoder decoder
model_path = f"models/autoencoders/encod_decod_{autoencoder_name}{model_format}"
model = load_model(model_path)  # If saved as .keras file
model = (
    create_encod_decod()
)  # If loading weights into the model, to dodge the lambda layer-caused loading issue
model.load_weights(model_path)
model.summary(expand_nested=False)

# Get decoder
encod, decod = split_encoder_decoder(encoder_decoder_model=model)  # If sequential model
encod = Model(  # If using keras.models Model API
    model.layers[0].input, model.get_layer("encoder").output[0]
)  # Get z_mean, the expectation of latent representation, as output
encod.summary()

# Get encoder
decod = Model(model.get_layer("decoder").input, model.get_layer("decoder").output)
decod.summary()

# Create meshgrid: shapes are (100, 100) and (100, 100)
x_coordinates, y_coordinates = create_meshgrid(encod=encod, flatten_data=True)

# Stack x_coordinates and y_coordinates to create a grid of data points
# in latent space of shape (100, 100, 2)
# (We are cautious with array manipulation here)
data_points_grid = np.stack([x_coordinates, y_coordinates], axis=-1)

# Reshape meshgrid like a dataset for keras
grid_dataset = data_points_grid.reshape(10_000, 2)

# Decod grid
X_decod = decod.predict(grid_dataset)

# Reshape like an actual grid
meshgrid_decod = X_decod.reshape(100, 100, 28, 28)

# Save decoded meshgrid into array
np.save(f"models/decoded_meshgrid/decod_grid_{autoencoder_name}", meshgrid_decod)
