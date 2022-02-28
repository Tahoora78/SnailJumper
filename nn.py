import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        self.w0 = np.random.randn(layer_sizes[1], layer_sizes[0])
        self.b0 = np.random.randn(layer_sizes[1], 1)
        self.hidden_layer = np.zeros((layer_sizes[1], 1))
        self.w1 = np.random.randn(layer_sizes[2], layer_sizes[1])
        self.b1 = np.random.randn(layer_sizes[2], 1)
        self.output_layer = np.zeros((layer_sizes[2], 1))

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here
        # )
        leaky_relu_x = np.where(x > 0, x, x * 0.01)
        return leaky_relu_x

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        self.hidden_layer = self.activation((self.w0 @ x) + self.b0)
        self.output_layer = self.activation(
            (self.w1 @ self.hidden_layer) + self.b1)


