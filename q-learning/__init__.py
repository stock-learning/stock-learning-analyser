import sys
from functions import *
from neural_network import build, load
from agent import Agent

def _evolutate(agent, data, data_len, n_inputs, n_episode, batch_size=32, is_replay = False):
    _state = get_state(data, 0, n_inputs + 1)
    _total_profit = 0
    agent._inventory = list()
    
    for T in range(data_len):
        _action = agent.action(_state)
        _next_state = get_state(data, T + 1, n_inputs + 1)
        _reward = 0

        if _action == 1: #buy
            agent._inventory.append(data[T])
            print(f'Buy: {format_currency(data[T])}')
        
        elif _action == 2 and len(agent._inventory) > 0: #sell
            _bought_price = agent._inventory.pop(0)
            _reward = max(data[T] - _bought_price, 0)
            _total_profit += data[T] - _bought_price
            print(f'Sell: {format_currency(data[T])} | Profit: {format_currency(data[T] - _bought_price)}')

        _done = T == data_len - 1
        agent._memory.append((_state, _action, _reward, _next_state, _done))
        _state = _next_state

        if _done:
            print('--------------------------------')
            print(f'Total Profit: {format_currency(_total_profit)}')
            print('--------------------------------')
        
        if is_replay and len(agent._memory) > batch_size:
            agent.replay(batch_size)

def _train(agent, data, data_len, n_inputs, n_episode):
    for episode in range(n_episode + 1):
        print(f'Episode {str(episode)}/{str(n_episode)}')
        _evolutate(agent, data, data_len, n_inputs, n_episode, is_replay=True)
        if episode % 10 == 0:
            agent._model.save(f'models/model_ep{str(episode)}')

if __name__ == "__main__":
    if sys.argv[1] == 'train':
        print('starting training...')
        _stock_name, _n_inputs, _n_episode = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        _neural_network = build(_n_inputs)
        _is_train = True
        _func = _train
    elif sys.argv[1] == 'evolutate':
        print('starting evolutate...')
        _stock_name, _model_name = sys.argv[2], sys.argv[3]
        _neural_network = load(_model_name)
        _n_inputs = _neural_network.layers[0].input.shape.as_list()[1]
        _is_train = False
        _n_episode = None
        _func = _evolutate
    else:
        exit()

    _agent = Agent(_neural_network, _is_train)
    _data = get_dataframe(_stock_name)
    _data = get_closing_values(_data)
    _func(_agent, _data, len(_data) - 1, _n_inputs, _n_episode)