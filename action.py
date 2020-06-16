# Author: Carlos Henrique Ponciano da Silva
import neural_network
import functions

import warnings
warnings.filterwarnings("ignore")

class Action:
    
    def __init__(self, server, api_stub):
        self._server = server
        self._api_stub = api_stub
        self._db = functions.connect_mongo()
        self._prediction_collection = 'prediction_data'
        self._training_collection = 'training_data'

    def initialize_daily_prediction(self):
        self._db[self._prediction_collection].remove({})
        self._api_stub.get_daily_companies()
    
    def finalize_daily_prediction(self):
        self._db[self._training_collection].remove({})
        self._api_stub.get_all_companies()

    def add_record_in_real_time(self, is_predict, stocks):
        _collection, _action = (self._prediction_collection, self._predict) if is_predict else (self._training_collection, self._train)
        self._db[_collection].insert_many(stocks)
        for stock_name in functions.get_all_stocks_initials(stocks):
            print(f'#### analyzing: {stock_name}')
            _data = functions.load_dataframe(_collection, stock_name)
            _data = functions.apply_standardization(_data)
            _action(_data, stock_name)
            print(f'#### analysis finished: {stock_name} \n')

    def _save_predict(self, initials, output_predict):
        self._api_stub.live_prediction({
            'initials': initials,
            'averageHit': output_predict['hit'].mean(),
            'totalReturn': output_predict['investment_value'].sum(),
            'buyHold': output_predict['return'].sum(),
            'updateDate': functions.get_current_datatime()
        })

        for movement in output_predict['convert_movements']:
            self._api_stub.live_prediction_movement({
                'initials': initials,
                'isSell': movement
            })

    def _predict(self, data, stock):
        print(f'predict: {stock}')
        _initials = functions.get_stock_name(stock)
        _test_x, _test_y = functions.get_only_normalized_values(data, return_real_value=True, to_numpy=False)
        _model = neural_network.load(_initials)
        _predict = _model.predict(_test_x)
        _predict = functions.inverse_transform(_predict)
        _output_predict = functions.create_value_output(_test_y, _predict)
        self._save_predict(_initials, _output_predict)

    def _train(self, data, stock, _epochs=1000, _batch_size=128, _verbose=0, _optimizer='adam', _loss='mean_squared_error'):
        print(f'train: {stock}')
        _train_x, _train_y, _test_x, _test_y = functions.splitting(data)
        _model = neural_network.build(_train_x.shape[1])
        _model.compile(optimizer=_optimizer, loss=_loss)
        _model.fit(_train_x, _train_y, epochs=_epochs, batch_size=_batch_size, validation_data=(_test_x, _test_y), verbose=_verbose)
        _model.save(f'models/model_{stock}')