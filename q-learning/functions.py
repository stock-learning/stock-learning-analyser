###
### standard functions for running the algorithm
###
from pymongo import MongoClient
import numpy as np
import math
import pandas as pd
from setting import get_env

def connect_mongo():
    return MongoClient(get_env('MONGO_HOST'), int(get_env('MONGO_PORT')))

def format_currency(value):
    _prefix = '-$' if value < 0 else '$'
    value = '{0:.2f}'.format(abs(value))
    return f'{_prefix}{value}'

def sigmoid(X):
    return 1 / (1 + math.exp(-X))

def get_dataframe(collection_name):
    _db = connect_mongo().predictions
    _collection = _db[collection_name]
    _df = pd.DataFrame(list(_collection.find()))
    _df.drop('_id', inplace=True, axis=1)
    return _df

def get_closing_values(dataframe):
    return list(dataframe['Close'])

def get_state(data, T, n):
    _d = T - n + 1
    _block = data[_d:T+1] if _d >= 0 else -_d * [data[0]] + data[0:T+1]
    _state = [sigmoid(_block[i+1] - _block[i]) for i in range(n - 1)]
    return np.array([_state])