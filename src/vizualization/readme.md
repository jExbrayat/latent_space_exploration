- ``color_meshgrid_based_on_pred.py`` generates an image - under *.png* and *.npy* formats - of a colored background for the user app. The background is colored based on the class of the decoded image of the corresponding two dimensional data point on the latent space meshgrid. 

- ``make_autoencoders_comparison.py`` is a callable python script that reads ``models\models_comparison\autoencoders_score.pkl`` file - which stores autoencoders loss scores - and products a barplot for model comparison at ``models\models_comparison\models_comparison_mse.png``.

- ``plot_dataset_on_latent_space.py`` encodes all MNIST images and plot their two-dimensional latent representation, for a specified autoencoder. Resulting plot is stored at ``models\latent_space_viz\actual_data_scatter_plot``. 