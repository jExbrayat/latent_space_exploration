from keras.models import load_model

from src.models.split_encoder_decoder import split_encoder_decoder
from src.utils.model_viz import fancy_summary

# TODO: write code as a function

summary_save_folder = "models/summaries"
autoencoders_folder = "models/autoencoders"

for autoencoder in ["ConvDense-5"]:
    autoencoder_path = f"{autoencoders_folder}/encod_decod_{autoencoder}.keras"
    encod_decod = load_model(autoencoder_path)
    encod, decod = split_encoder_decoder(encod_decod)
    encod_summary = fancy_summary(encod)
    decod_summary = fancy_summary(decod)
    with open(f"{summary_save_folder}/{autoencoder}.txt", "a") as f:
        print("Encoder", file=f)
        print(encod_summary, file=f)
        print("", file=f)
        print("Decoder", file=f)
        print(decod_summary, file=f)
