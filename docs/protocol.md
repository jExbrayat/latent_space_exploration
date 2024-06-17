# Protocol
This file logs my thoughts and describes my objectives.

## Low loss vs right meshgrid decoding
Dense-1 autoencoder performs less than ConDense-2 autoencoder altough Dense-1 gives much better decoding on the meshgrid of latent space.  
I.e. ConvDense-2 manage better to autoencode MNIST data, but fails at the **task we are trying to achieve in this repository, that is to display a 100x100 grid of the 2-dimensional latent space with decoded image of each point of the grid**.  

There may be two reasons for that:  
- Decoder overfits actual data and thus fails to generalize on the whole meshgrid.  
- Encoder concentrates data points in small portions of latent space, making a uniformly sparsed meshgrid innapropriate.  

## Method
We aim for a good autoencoder, with low loss, and a fancy latent space display on a square grid, colored based on predictions of a classifier.  
Thus, we will try to achieve better than the first naive model Dense-1, even if it gives good results in the end.  

1) Plot latent space representations of actual MNIST images to see their distribution on latent space.  
See ``models/latent_space_viz/actual_data_scatter_plot/ConvDense-2_encoder.png``  
As expected, the encoder does not create a square-shaped latent space but something like a diagonal. Hence the bad decoding on the meshgrid outside the diagonal.  

1) Build a model that produces a square-shaped latent space.  

2) Decode each point of latent space meshgrid to plot them interactively in user app.  
Result is at ``models/decoded_meshgrid``

1) Create a colormap of the meshgrid based on the predicted classes of the decoded images.  
See ``models/latent_space_viz/colormaps``  
This task is done thanks to a classifier trained on MNIST images.  
**Recall on data structure:**  
(28, 28) MNIST image --*encoder*--> 2D representation of MNIST image --*decoder*--> (28, 28) decoded image

1) Create a user app to visualize the latent space colored based on represented number and its decoded version beside.  

## How to make a good encoder according to experimentations  
Experimentations led to the following clues to get proper latent space:
- Use tanh or sigmoid activation functions for the output.
- ~~The longer the training, the less evenly distributed on the axis of latent space the data points are.~~  
Wrong: using proper activation function for output of encoder and using validation set works fine.
- Max pooling layers seem to destroy too much information since resulting loss is high.  
- Expanding latent space with convolutional layers on top improves autoencoder loss.
- Use validation set to avoid overfitting.
- Dropout layers make autoencoder's performance lower while not ensuring an evenly distributed latent space on two axis. 