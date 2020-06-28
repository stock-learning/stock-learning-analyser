# Author: Carlos Henrique Ponciano da Silva
from keras import models
from keras import layers
from keras.layers import Dense


# create a new model from scratch
# three-layer model with n inputs using the activation function relu
def build(n_input, verbose=0):
    model = models.Sequential()
    model.add(layers.Dense(30, input_dim = n_input, activation = "relu"))
    model.add(layers.Dense(30, activation ="relu"))
    model.add(layers.Dense(30, activation ="relu"))
    model.add(layers.Dense(1))

    if verbose:  
        model.summary()
        
    return model

# loads a model already exist in memory
def load(model):
    return models.load_model(f'models/model_{model}')