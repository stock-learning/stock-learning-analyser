import keras
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
from setting import get_env


# neural network with four hidden layers
def build(n_inputs):
    _model = Sequential()
    _model.add(Dense(units=64, input_dim=n_inputs, activation="relu"))
    _model.add(Dense(units=32, activation="relu"))
    _model.add(Dense(units=8, activation="relu"))
    _model.add(Dense(int(get_env('NUMBER_LAYER_EXISTS')), activation="linear"))
    _model.compile(loss=get_env('LOSS'), optimizer=Adam(lr=float(get_env('LR'))))
    return _model

def load(model):
    return load_model(f'models/{model}')