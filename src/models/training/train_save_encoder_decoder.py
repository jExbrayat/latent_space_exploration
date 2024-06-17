# Check result
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping, History, ModelCheckpoint
from keras.models import save_model

import src.utils.model_viz as model_viz
from src.data.import_data import import_data
from src.models.define_model import create_encod_decod

# Define reference name
saving_file_name = "encod_decod_VAE-1"

# Define batch size
batch_size = 2048

# Import data
X, y, y_categorical = import_data(flatten=True)

# Define encoder decoder model
encod_decod = create_encod_decod()
encod_decod.summary(expand_nested=True)

# Compile
encod_decod.compile(optimizer="adam")

# Define callbacks
stopper = EarlyStopping(monitor="val_loss", patience=30, restore_best_weights=True)
checkpoint = ModelCheckpoint(
    filepath=f"models/checkpoints/{saving_file_name}/epoch_{'{epoch:02d}'}.keras",
    save_freq=(len(X) // batch_size) * 10,  # Save model every 10 epochs
)
history = History()

# Train model
encod_decod.fit(
    X,
    X,
    batch_size=batch_size,
    epochs=1000,
    callbacks=[stopper, checkpoint, history],
    validation_split=0.2,
)

# Vizualize model training curves
model_viz.plot_training_curve(
    training_loss=history.history["loss"],
    validation_loss=history.history["val_loss"],
    plot_from_n_epoch=0,
    save_path=f"models/training_curves/{saving_file_name}_training.png",
)

# Save encoder decoder
save_model(encod_decod, f"models/autoencoders/{saving_file_name}.keras")
encod_decod.save_weights(f"models/autoencoders/{saving_file_name}.h5")


X_pred = encod_decod.predict(X)
for idx in range(10):
    _, axs = plt.subplots(2, 1)
    img = X[idx].reshape(28, 28)
    img_pred = X_pred[idx].reshape(28, 28)
    axs[0].imshow(img)
    axs[1].imshow(img_pred)
    plt.show()
    plt.close()
