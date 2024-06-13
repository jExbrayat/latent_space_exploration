import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Dense, Layer


def plot_training_curve(
    training_loss: list,
    plot_from_n_epoch: int,
    validation_loss: list = [],
    validation_accuracy: list = None,
    save_path: str = None,
    logscale: bool = True,
) -> None:
    """Plot training curves of a keras model
    (train loss, val loss, val accuracy if classification model)

    Args:
        training_loss (list): training loss
        gathered from history callback

        validation_loss (list): validation loss
        gathered from history callback

        validation_accuracy (list): validation accuracy gathered
        from history callback

        plot_from_n_epoch (int): epoch from which to plot when there are too many
        save_path (str): path to save plot in .png format
    """

    num_epochs_to_display = len(training_loss) - plot_from_n_epoch
    step_x_ticks = (
        int(num_epochs_to_display / 10) if int(num_epochs_to_display / 10) >= 1 else 1
    )

    plt.plot(training_loss[plot_from_n_epoch:], label="training loss")
    plt.plot(validation_loss[plot_from_n_epoch:], label="validation loss")

    if validation_accuracy is not None:
        plt.plot(validation_accuracy[plot_from_n_epoch:], label="validation accuracy")

    if logscale:
        plt.yscale("log")

    plt.legend()
    plt.title("training curve")

    plt.xticks(
        np.arange(0, num_epochs_to_display, step=step_x_ticks),
        np.arange(
            plot_from_n_epoch + 1,
            plot_from_n_epoch + num_epochs_to_display + 1,
            step=step_x_ticks,
        ),
    )

    if save_path is not None:
        plt.savefig(save_path)

    plt.show()


def get_layer_activation(layer):
    if isinstance(layer, Layer):
        return layer.activation.__name__ if hasattr(layer, "activation") else "None"
    else:
        return "None"


def get_layer_neurons(layer):
    if isinstance(layer, Dense):
        return layer.get_weights()[0].shape[1]
    else:
        return "N/A"


def fancy_summary(model):
    summary_text = ""
    summary_text += f"{'Layer':<20} {'Output Shape':<20} {'Neurons':<10} {'Param #':<20} {'Activation':<20}\n"
    summary_text += "=" * 100 + "\n"
    total_params = 0
    for layer in model.layers:
        output_shape = layer.output_shape[1:]
        param_count = layer.count_params()
        neurons = get_layer_neurons(layer)
        activation = get_layer_activation(layer)
        summary_text += f"{layer.name:<20} {str(output_shape):<20} {neurons:<10} {param_count:<20} {activation:<20}\n"
        total_params += param_count
    summary_text += "=" * 100 + "\n"
    summary_text += f"Total params: {total_params}"

    return summary_text
