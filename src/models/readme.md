- ``define_model.py`` defines python functions to create autoencoder and classifier models for this repository.  

- ``split_encoder_decoder.py`` defines python function to separate the encoding and the decoding part of an autoencoder.

- ``evaluate_model.py`` is a callable script to evaluate an autoencoder performance (mean squared error between original image and its autoencoded version) and store it into ``models\models_comparison\autoencoders_score.pkl`` (pickle file readable with *pickle* python library).

- ``make_models_complete_summary.py`` logs a detailed summary for each autoencoder in ``./models/summaries`` under *.txt* format.

- ``decod_meshgrid.py`` is a script for predicting all data points of a meshgrid of shape (100, 100) of an autoencoder's latent space. Each prediction is thus an image of shape (28, 28). All predictions are stored in a *.npy* file - readable with numpy - in ``models/decoded_meshgrid``.