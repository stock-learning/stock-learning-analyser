# Author: Carlos Henrique Ponciano da Silva
from action import Action


class RealTimeValueAdditionHandler(Action):

    def __init__(self, server, api_stub):
        super().__init__(server, api_stub)
        self.primitive_name = 'real-time-value-addition-handler'

    def consume(self, message):
        try:
            self.add_record_in_real_time(bool(message['isPredict']), message['stocks'])
        except Exception as ex:
            print(ex)