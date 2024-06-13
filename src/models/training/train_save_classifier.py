from keras.callbacks import EarlyStopping, History
from keras.models import load_model, save_model

import src.utils.model_viz as model_viz
from src.data.import_data import import_data
from src.models.define_model import create_classifier
from src.models.split_encoder_decoder import split_encoder_decoder

# Import data
X, y, y_categorical = import_data()

# Define classifier
classifier = create_classifier()
classifier.summary()

# Compile classifier
classifier.compile(
    loss="categorical_crossentropy", optimizer="adam", metrics="accuracy"
)

# Define callbacks
stopper = EarlyStopping(monitor="val_loss", patience=15, restore_best_weights=True)
classifier_history = History()

# Train model
classifier.fit(
    X,
    y_categorical,
    batch_size=512,
    epochs=10,
    callbacks=[stopper, classifier_history],
    validation_split=0.2,
)

# Vizualize model training curves
model_viz.plot_training_curve(
    training_loss=classifier_history.history["loss"],
    validation_loss=classifier_history.history["val_loss"],
    plot_from_n_epoch=0,
    save_path="models/training_curves/classifier_training.png",
)

# Save encoder decoder
save_model(classifier, "models/classifier.keras")
