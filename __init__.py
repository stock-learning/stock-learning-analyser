# Author: Carlos Henrique Ponciano da Silva
import neural_network
import functions

import warnings
warnings.filterwarnings("ignore")

def training(action_name='bvsp_train', _epochs=1000, _batch_size=128, _verbose=0, _optimizer='adam', _loss='mean_squared_error'):
    _data = functions.load_dataframe(action_name)
    _data = functions.apply_standardization(_data)
    _train_x, _train_y, _test_x, _test_y = functions.splitting(_data)
    _model = neural_network.build(_train_x.shape[1])
    _model.compile(optimizer=_optimizer, loss=_loss)
    _model.fit(_train_x, _train_y, epochs=_epochs, batch_size=_batch_size, validation_data=(_test_x, _test_y), verbose=_verbose)
    _model.save(f'models/model_{functions.get_action_name(action_name)}')

def production(action_name='bvsp_test'):
    _data = functions.load_dataframe(action_name)
    _data = functions.apply_standardization(_data)
    _test_x, _test_y = functions.get_only_normalized_values(_data, return_real_value=True, to_numpy=False)
    _model = neural_network.load(functions.get_action_name(action_name))
    _predict = _model.predict(_test_x)
    _predict = functions.inverse_transform(_predict)
    return functions.create_value_output(_test_y, _predict)  

if __name__ == '__main__':
    # training()
    Y = production()
    print(f'Average hit: {Y["Hit"].mean()}') #Media de certo
    print(f'Total return value of our strategy:  R${Y["Investment_Value"].sum()}') # valor de retorno da estrategia
    print(f'Buy & Hold: R${Y["Return"].sum()}')  # estratégia Buy&Hold