# general content libraries for the class
import numpy as np
import random
from setting import get_env
from collections import deque


class Agent(object):

    def __init__(self, model, is_train):
        self._model = model
        self._is_train = is_train
        self._memory = deque(maxlen=1000)
        self._inventory = list()

        #env
        self._central_limit = float(get_env('CENTRAL_LIMIT'))
        self._minimum_limit = float(get_env('MINIMUM_LIMIT'))
        self._fall_limit = float(get_env('FALL_LIMIT'))
        self._n_layer_exists = int(get_env('NUMBER_LAYER_EXISTS'))
        self._gamma = float(get_env('GAMMA'))

    def action(self, state):
        if self._is_train and random.random() <= self._central_limit:
            return random.randrange(self._n_layer_exists)
        return np.argmax(self._model.predict(state)[0])

    def replay(self, size):
        _memory_size = len(self._memory)
        _batch = [self._memory[i] for i in range(_memory_size - size + 1, _memory_size)]

        for state, action, reward, next_state, done in _batch:
            _target = reward
            if not done:
                _target += self._gamma * np.amax(self._model.predict(next_state)[0])

            _current_target = self._model.predict(state)
            _current_target[0][action] = _target
            self._model.fit(state, _current_target, epochs=1, verbose=0)
        
        if self._central_limit > self._minimum_limit:
            self._central_limit *= self._fall_limit