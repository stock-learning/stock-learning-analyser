# Author: Carlos Henrique Ponciano da Silva
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from setting import get_env

# general variables
_scaler = None

# connects to the database
def connect_mongo():
    return MongoClient(get_env('MONGO_HOST'), int(get_env('MONGO_PORT')))

# get the correct name
def get_action_name(action_name):
    if '_' in action_name:
        return action_name.split('_')[0]
    return action_name

# loads the dataframe from the database
def load_dataframe(collection_name):
    _db = connect_mongo()[get_env('DATABASE')]
    _collection = _db[collection_name]
    _data = pd.DataFrame(list(_collection.find()))
    _data.drop('_id', inplace=True, axis=1)
    return _data

# normalizes data between 0 and 1 for better neural network performance
def apply_standardization(data):
    global _scaler
    _scaler = StandardScaler()

    data['Close_Tomorrow'] = data['Close'].shift(-1)
    data['Return'] = data['Close_Tomorrow'] - data['Close']
    
    for c in data.columns:
        data[c+'_Norm'] = _scaler.fit_transform(data[c].to_numpy().reshape(-1, 1))

    return data.dropna()

# get normalized data
def get_only_normalized_values(data, return_real_value=False, to_numpy=True):
    _x = data[['Open_Norm','High_Norm','Low_Norm','Close_Norm','Volume_Norm']]

    if return_real_value:
        _y = data[['Return_Norm', 'Return']]
    else:
        _y = data[['Return_Norm']]

    if to_numpy:
        return _x.to_numpy(), _y.to_numpy()

    return _x, _y

# separate training and test data
def splitting(data, percentage=0.2):
    _size_data = len(data)
    _amount_training = _size_data - int(_size_data * percentage)
    _train_x, _train_y = get_only_normalized_values(data[:_amount_training])
    _test_x, _test_y = get_only_normalized_values(data[_amount_training + 1:])
    return _train_x, _train_y, _test_x, _test_y

# invert the data matrix
def inverse_transform(data):
    global _scaler
    return _scaler.inverse_transform(data)

# mounts at the output of the dataframe
def create_value_output(Y, predicts):
    Y['Return_Predictions'] = predicts
    Y['Prediction_Movements'] = ['Up' if predict > 0 else 'Down' for predict in predicts]
    Y['Real_Movements'] = [ 'Up' if y > 0 else 'Down' for y in Y['Return']]
    Y['Hit'] = [ 1 if y[1]['Real_Movements'] == y[1]['Prediction_Movements'] else 0 for y in Y.iterrows()]
    Y['Investment_Value'] = [y[1]['Return'] if y[1]['Prediction_Movements'] == 'Up' else 0 for y in Y.iterrows()]
    return Y