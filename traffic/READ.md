# Experimentation Insights
Here are my most notable observations I encountered while playing around with the different conditions and values in my CNN: 

### gtsrb-small Dataset:
- 16 kernels > 32 kernels > 8 kernels > 4 kernels (as of accuracy in my smaller dataset)
- Similar results as above occure with the amount of neurons in hidden layers (my best result with 64) 
- Sigmoid in the hidden layers results in higher accuracy when using more hidden layers as ReLu and ReLu when using less
- The highest accuracy I achieved on the small model was 1.0000 (loss: 0.0054) with just 1 Convolutional layer (16 3x3 kernels, ReLu) followed by 2x2 max pooling and then a hidden layer (64, ReLu) before the output layer (Softmax). However, this model resulted in terrible classification when using the large dataset

### gtsrb Dataset:
- Got my highest accuracy (0.87) here as implemented in the code.
- Better numbers with more kernels and larger hidden layers than in the smaller set. But too many also make it worse.
- Nadam optimizer was roughly 30% more accurate than traditional Adam here
- ReLu seems to be more effective in convolutional layers while sigmoid's better in the hidden ones