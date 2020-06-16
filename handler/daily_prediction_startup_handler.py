# Author: Carlos Henrique Ponciano da Silva
from action import Action


class DailyPredictionStartupHandler(Action):

    def __init__(self, server, api_stub):
        super().__init__(server, api_stub)
        self.primitive_name = 'daily-prediction-startup-handler'

    def consume(self, message):
        try:
            self.initialize_daily_prediction()
        except Exception as ex:
            print(ex)