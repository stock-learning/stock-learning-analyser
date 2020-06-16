# Author: Carlos Henrique Ponciano da Silva
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from setting import get_env
from datetime import datetime

# general variables
_scaler = None

# connects to the database
def connect_mongo():
    return MongoClient(get_env('MONGO_HOST'), int(get_env('MONGO_PORT')))[get_env('DATABASE')]

# get the correct name
def get_stock_name(stock_name):
    if '_' in stock_name:
        return stock_name.split('_')[0]
    return stock_name

# loads the dataframe from the database
def load_dataframe(collection, stock):
    _db = connect_mongo()
    _collection = _db[collection]
    _data = pd.DataFrame(list(_collection.find({'name': {'$eq': stock}}, {'_id': 0, 'name': 0})))
    return _data

# normalizes data between 0 and 1 for better neural network performance
def apply_standardization(data):
    global _scaler
    _scaler = StandardScaler()

    data['close_Tomorrow'] = data['close'].shift(-1)
    data['return'] = data['close_tomorrow'] - data['close']
    
    for c in data.columns:
        data[c+'_norm'] = _scaler.fit_transform(data[c].to_numpy().reshape(-1, 1))

    return data.dropna()

# get normalized data
def get_only_normalized_values(data, return_real_value=False, to_numpy=True):
    _x = data[['open_norm','high_norm','low_norm','close_norm','volume_norm']]

    if return_real_value:
        _y = data[['return_norm', 'return']]
    else:
        _y = data[['return_norm']]

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
    Y['return_predictions'] = predicts
    Y['prediction_movements'] = ['Up' if predict > 0 else 'Down' for predict in predicts]
    Y['convert_movements'] = [0 if predict > 0 else 1 for predict in predicts]
    Y['real_movements'] = [ 'Up' if y > 0 else 'Down' for y in Y['return']]
    Y['hit'] = [ 1 if y[1]['real_movements'] == y[1]['prediction_movements'] else 0 for y in Y.iterrows()]
    Y['investment_value'] = [y[1]['return'] if y[1]['prediction_movements'] == 'Up' else 0 for y in Y.iterrows()]
    return Y

# get current date and time
def get_current_datatime():
    return datetime.now()