from keras import backend as K
from keras.layers import (
    Dense,
    Dropout,
    Input,
    Lambda,
)
from keras.losses import mean_squared_error
from keras.models import Model


def variational_sampling(args: tuple) -> list:

    # Get arguments
    z_mean, z_log_sigma = args
    # Compute epsilon, the gaussian component
    epsilon = K.random_normal(
        shape=(K.shape(z_mean)[0], latent_dim), mean=0.0, stddev=0.1
    )
    # Compute the random sample
    random_sample = z_mean + K.exp(z_log_sigma) * epsilon

    return random_sample


# Init parameters
original_dim = 28 * 28
latent_dim = 2
inputs = Input(shape=(original_dim,))


def create_encod():

    # Create encoder
    hidden = Dense(units=128, activation="relu")(inputs)
    hidden = Dropout(0.2)(hidden)
    hidden = Dense(units=64, activation="relu")(hidden)
    hidden = Dropout(0.2)(hidden)
    hidden = Dense(units=32, activation="relu")(hidden)
    hidden = Dropout(0.2)(hidden)
    hidden = Dense(units=8, activation="relu")(hidden)
    z_mean = Dense(units=latent_dim, activation="sigmoid")(hidden)
    z_log_sigma = Dense(latent_dim)(hidden)
    z = Lambda(variational_sampling)(
        [z_mean, z_log_sigma]
    )  # Compute a sample on latent space
    encoder = Model(inputs, [z_mean, z_log_sigma, z], name="encoder")

    return encoder


def create_decod():

    # Create decoder
    latent_inputs = Input(shape=(latent_dim,), name="z_sampling")
    hidden = Dense(units=8, activation="relu")(latent_inputs)
    hidden = Dense(units=32, activation="relu")(hidden)
    hidden = Dense(units=64, activation="relu")(hidden)
    hidden = Dense(units=128, activation="relu")(hidden)
    outputs = Dense(original_dim, activation="sigmoid")(hidden)
    decoder = Model(latent_inputs, outputs, name="decoder")

    return decoder


def create_encod_decod():

    encoder = create_encod()
    decoder = create_decod()

    # Create autoencoder
    variational_encoder_outputs = encoder(inputs)[2]
    autoencoder_outputs = decoder(variational_encoder_outputs)
    autoencoder = Model(inputs, autoencoder_outputs, name="variational_autoencoder")

    # Customize loss function
    reconstruction_loss = mean_squared_error(inputs, autoencoder_outputs)
    # reconstruction_loss *= original_dim TODO: is this necessary ?
    # It allows to greatly increase reconstruction loss importance. It is possible to apply a little coefficient to kl_loss instead
    z_mean, z_log_sigma = encoder(inputs)[0], encoder(inputs)[1]
    kl_loss = -1 - z_log_sigma + K.square(z_mean) + K.exp(z_log_sigma)
    kl_loss = K.sum(kl_loss, axis=-1)  # Sum over latent space dimensions
    kl_loss *= 0.001
    vae_loss = reconstruction_loss + kl_loss
    autoencoder.add_loss(vae_loss)

    return autoencoder
