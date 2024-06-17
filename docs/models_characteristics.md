# Model Characteristics

This file summarizes the architectures of the models tried in this repository.  
Model performance comparisons are available here: ``models/models_comparison/models_comparison.png``  
If the specifications below are not precise enough, the models' architectures can be found in the ``models/summaries`` folder.

## Naive Dense Network with 4 Layers
*``models/autoencoders/encod_decod_Dense-1.keras``*  
First attempt at a dense layer autoencoder with sigmoid activation functions.  
It performs surprisingly well.

## Improved Dense Network
*``models/autoencoders/encod_decod_Dense-2.keras``*  
This dense network features dropout layers and sigmoid activation functions for outputs, and tanh activation for hidden layers.  
It adds a hidden layer of 64 neurons.  
It performs just as well as the first dense model.

## CNN-1
*``models/autoencoders/encod_decod_CNN.keras``*  
First attempt at a convolutional network with *Conv2D* and *MaxPooling* layers.  
Training failed as the encoder sets all values close to zero, causing the decoder to always give the same output.  
The loss function is not very high, yet the gradient descent seems stuck in a local minimum, with the encoder setting every pixel to zero in the latent space.  
All activation functions are relu.

## CNN-2
*``models/autoencoders/encod_decod_CNN-2.keras``*  
Retraining of CNN-1.  
It performs surprisingly poorly, despite being theoretically more suitable than dense layers for image processing.  
All activation functions are relu.

## CNN-3
*``models/autoencoders/encod_decod_CNN-3.keras``*  
Third attempt at a convolutional network.  
This architecture features dropout layers and validation split during training to prevent the encoder from "destroying encoding."  
Training succeeded, but the loss is still higher than that of the first naive dense model.

## Hybrid Convolutional-Dense Network

1. **First try**  
   *``models/autoencoders/encod_decod_ConvDense.keras``*  
   Instead of downsizing the latent representation into two dimensions with max pooling layers, the hybrid model uses a first convolutional layer for data augmentation and then reduces dimensions with max pooling and dense layers.  
   Relu activation functions only.  
   The hybrid model performs better than any fully convolutional network.  
   Very surprisingly, its latent space is only one-dimensional, as the second dimension sets all values to zero.

2. **Second try**  
   **Meta model** *``models/autoencoders/encod_decod_ConvDense-2.keras``*  
   No more max pooling layers, only dense layers for dimension reduction from augmented data with a first convolutional layer.  
   Relu activation functions only.  
   Performance is even better.  
   **Tuned decoder** *``models/autoencoders/encod_decod_ConvDense-2_tuned_decoder.keras``* using *``models/autoencoders/decod_Dense-2.keras``* decoder  
   The decoder layer of this model was specifically trained to decode latent representations of the meta model encoder.  
   Training was done with validation split to prevent overfitting. Generalization is needed on the meshgrid.

3. **Third try**  
   *``models/autoencoders/encod_decod_ConvDense-3.keras``*  
   This model combines *relu*, *sigmoid*, and *tanh* activation functions.  
   It also has 32 filters (vs 16) as output to the data augmentation convolutional layer and more parameters in the dense layers.  
   Training takes a lot of time compared to lighter models: up to 1 minute per epoch!  
   The gradient seems more likely to get stuck in local minima, leading to potentially never achieving convergence. Hence the relatively high loss compared to the lighter hybrid model.

4. **Fourth try**  
   *``models/autoencoders/encod_decod_ConvDense-4.keras``*  
   A lighter version of the hybrid convolutional-dense model with only 4 filters and fewer neurons in dense layers.  
   Training is fast and avoids time spent in local minima.  
   However, the loss is greater than the intermediary model (second try).

5. **Fifth try**  
   *``models/autoencoders/encod_decod_ConvDense-5.keras``*  
   Same architecture as *ConvDense-2*, but with tanh activation for the encoder output to achieve a more square-shaped latent space.  
   It performs just as well as the *ConvDense-2* autoencoder.

## n8python's Version
*n8python is the original author of the MNIST Latent Space project.*  

Autoencoder training failed because the encoder encodes every image to the same two-dimensional point (-1, 1).
