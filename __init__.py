# Author: Carlos Henrique Ponciano da Silva
from stock_learning_rabbitmq.ApiStub import ApiStub
from stock_learning_rabbitmq.RabbitMQServer import RabbitMQServer
from handler.daily_prediction_startup_handler import DailyPredictionStartupHandler
from handler.daily_prediction_closing_handler import DailyPredictionClosingHandler
from handler.real_time_value_addition_handler import RealTimeValueAdditionHandler
from setting import get_env


if __name__ == '__main__':
    print('initialized server...')
    _server = RabbitMQServer(get_env('QUEUE_NAME'), get_env('RABBIT_HOST'))
    _api_stub = ApiStub(_server)

    print('registering handlers...')
    _server.register(DailyPredictionStartupHandler(_server, _api_stub))
    _server.register(DailyPredictionClosingHandler(_server, _api_stub))
    _server.register(RealTimeValueAdditionHandler(_server, _api_stub))

    print('Initialized and waiting...')
    _server.disable_heartbeat()
    _server.start_listening()