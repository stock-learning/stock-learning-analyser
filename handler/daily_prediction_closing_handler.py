# Author: Carlos Henrique Ponciano da Silva
from action import Action


class DailyPredictionClosingHandler(Action):

    def __init__(self, server, api_stub):
        super().__init__(server, api_stub)
        self.primitive_name = 'daily-prediction-closing-handler'

    def consume(self, message):
        self.finalize_daily_prediction()