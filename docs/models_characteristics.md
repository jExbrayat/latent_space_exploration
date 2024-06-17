# Models characteristics  
This file sums up the architecture of tried models of this repository.  
Models performance comparison is avaible here: ``models/models_comparison/models_comparison.png``  
In case bellow specifications are not precise enough, models' architecture can be found in ``models/summaries`` folder.  

## Naive dense network with 4 layers
``models/autoencoders/encod_decod_Dense-1.keras``  
First try of dense layers autoencoder with sigmoid activation functions.  
It performs surprisingly well.  

## Improved dense network
``models/autoencoders/encod_decod_Dense-2.keras``  
This dense network features dropout layers and sigmoid activation function for ouputs, tanh activation for hidden layers.  
It adds a hidden layer of 64 neurons.  
It performs just as well as the first dense model.

## CNN-1
``models/autoencoders/encod_decod_CNN.keras``  
First try of convolutional network with *Conv2D* and *MaxPooling* layers.  
Training failed as encoder sets all values close to zero. Thus decoder gives always the same output.  
Loss function is not so high yet.  
I think gradient descent was stuck in a local minimum corresponding to encoder setting every pixel to zero in latent space. 
All activation functions are relu.  

## CNN-2
``models/autoencoders/encod_decod_CNN-2.keras``  
Just a retraining of CNN-1.  
It performs surprisingly poorly as it should be more appropriate than dense layers for image processing.  
All activation functions are relu.  

## CNN-3
``models/autoencoders/encod_decod_CNN-3.keras``  
Third try of convolutional network.
This architectures features dropout layers and validation split during training to prevent encoder to *destroy encoding*.  
Training succeeded but loss is still higher than the first naive dense model.  

## Hybrid convolutional-dense network
1) First try to combine convolutional and dense layers  
``models/autoencoders/encod_decod_ConvDense.keras``  
Instead of downsizing latent representation into two dimensions with max pooling layers, the hybrid model uses a first convolutional layer for data augmentation and then reduces dimensions with max pooling and dense layers.  
Relu activation functions only.  
Hybrid model performs better than any fully convolutional network.  
Very surprisingly, its latent space is only one-dimensional since the second dimension sets all values to zero.

2) Second try  
**Meta model** ``models/autoencoders/encod_decod_ConvDense-2.keras``  
No more max pooling layers but only dense layers for dimension reduction from augmented data with a first convolutional layers.  
Relu activation functions only.    
Performance is even better.  
**Tuned decoder** ``models/autoencoders/encod_decod_ConvDense-2_tuned_decoder.keras`` using ``models/autoencoders/decod_Dense-2.keras`` decoder  
Decoder layer of this model was specifically trained to decod latent representations of the meta model encoder.  
Training was done with validation split in order to prevent the model from overfitting actual data. In fact generalization is needed on meshgrid. 

3) Third try  
``models/autoencoders/encod_decod_ConvDense-3.keras``  
This model combines *relu*, *sigmoid* and *tanh* activation functions.   
It also has 32 filters (*vs* 16) as output to data augmentation convolutional layer and more parameters in the dense layers.  
Training takes a lot of time compared to lighter models: up to 1 minute per epoch!  
Gradient seems to be more likely stuck in local minima. Thus, convergence may never happen. Hence the relatively high loss compared to the lighter hybrid model.

4) Fourth try  
``models/autoencoders/encod_decod_ConvDense-4.keras``  
Light version of hybrid convolutional-dense model with only 4 filters and fewer neurons in dense layers.  
Training is fast and without time spent in local minimum.  
However, loss is greater than the intermediary model (second try).

5) Fith try  
``models/autoencoders/encod_decod_ConvDense-5.keras``  
Same architecture as *ConvDense-2* except it features tanh activation for encoder output, in order to get a more square-shaped latent space.  
It performs just as well as *ConvDense-2* autoencoder.

## n8python's version
*n8python github user is the original author of MNIST Latent Space project.*  

Autoencoder training failed because encoder encodes every image to the same two-dimensional point (-1, 1).


