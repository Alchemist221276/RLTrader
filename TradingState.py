import os.path
from enum import Enum
import math
from TicksHistory import TicksHistory
import pickle


class tsValueAllowedPair:
    def __init__(self, value=0.0, allowed=False):
        self._value = value
        self._allowed = allowed

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)


    def get_allowed(self):
        return self._allowed

    def set_allowed(self, allowed):
        self._allowed = allowed

    allowed = property(get_allowed, set_allowed)


class tsOrderType(Enum):
    BuyStop     = 0,
    SellStop    = 1,
    BuyLimit    = 2,
    SellLimit   = 3,
    Buy         = 4,
    Sell        = 5


class tsOrder():
    def __init__(self, symbol, type, open_date, open_price, stoploss=None, takeprofit=None, close_date=None, close_price=None):
        self._symbol = symbol
        self._type = type
        self._open_date = open_date
        self._open_price = open_price
        self._stoploss = stoploss
        self._takeprofit = takeprofit
        self._close_date = close_date
        self._close_price = close_price
        self._max_loss = None
        self._max_profit = None
        self._history = []

    # TODO: Write properties implementation


class tsOrders():
    def __init__(self):
        self._orders = []

    def __len__(self):
        return len(self._orders)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        return self._orders[index]

    def get_orders(self):
        return self._orders.copy()

    orders = property(get_orders)


    def get_buystop_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.BuyStop:
                orders_list.append(order)
        return orders_list

    buystop_orders = property(get_buystop_orders)


    def get_sellstop_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.SellStop:
                orders_list.append(order)
        return orders_list

    sellstop_orders = property(get_sellstop_orders)


    def get_buylimit_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.BuyStop:
                orders_list.append(order)
        return orders_list

    buylimit_orders = property(get_buylimit_orders)


    def get_selllimit_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.SellStop:
                orders_list.append(order)
        return orders_list

    selllimit_orders = property(get_selllimit_orders)


    def get_buy_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.Buy:
                orders_list.append(order)
        return orders_list

    buy_orders = property(get_buy_orders)


    def get_sell_orders(self):
        orders_list = []
        for order in self._orders:
            if order.type == tsOrderType.Sell:
                orders_list.append(order)
        return orders_list

    sell_orders = property(get_sell_orders)


class tsOpenOrderAction:
    def __init__(self):
        self._allowed = False
        self._probability = 0.0
        self._open_price = 0.0
        self._stoploss = 0.0
        self._takeprofit = 0.0
        
    
    def get_allowed(self):
        return self._allowed
    
    def set_allowed(self, value):
        self._allowed = value
        
    allowed = property(get_allowed, set_allowed)
    
    
    def get_probability(self):
        return self._probability
    
    def set_probability(self, value):
        self._probability = value

    probability = property(get_probability, set_probability)
    
    
    def get_open_price(self):
        return self._open_price
    
    def set_open_price(self, value):
        self._open_price = value
        
    open_price = property(get_open_price, set_open_price)
    
    
    def get_stoploss(self):
        return self._stoploss
    
    def set_stoploss(self, value):
        self._stoploss = value
        
    stoploss = property(get_stoploss, set_stoploss)
    
    
    def get_takeprofit(self):
        return self._takeprofit
    
    def set_takeprofit(self, value):
        self._takeprofit = value
        
    takeprofit = property(get_takeprofit, set_takeprofit)


class tsParameters:
    def __init__(self):
        self._money_management = 0
        self._probability_threshold = 0.8
        self._open_orders = tsOrders()
        self._lot_size = 1.0
        self._spread = 0
        self._min_stoploss = 20
        self._min_takeprofit = 20
        self._buy = tsOpenOrderAction()
        self._sell = tsOpenOrderAction()
        self._buystop = tsOpenOrderAction()
        self._sellstop = tsOpenOrderAction()
        self._buylimit = tsOpenOrderAction()
        self._selllimit = tsOpenOrderAction()


    def get_probability_threshold(self):
        return self._probability_threshold

    def set_probability_threshold(self, threshold):
        self._probability_threshold = threshold

    probability_threshold = property(get_probability_threshold, set_probability_threshold)


    def get_open_orders(self):
        return self._open_orders
    
    open_orders = property(get_open_orders)

    # TODO: Write properties implementation


class tsState:
    def __init__(self, trading_state=None, prev_state=None):
        self._trading_state = trading_state
        self._parameters = tsParameters()
        self._open_orders = tsOrders()

        if prev_state is not None:
            self.init_from_prev_state(prev_state)

    def get_actions_probabilities(self):
        return self._actions_probabilities

    def get_parameters(self):
        return self._parameters

    actions_probabilities = property(get_actions_probabilities)
    parameters = property(get_parameters)

    def set_state_allowed_elements(self, prev_state):
        if not prev_state['parameters']['buy'] and not not prev_state['parameters']['sell']:
            self._actions_probabilities['buy']['allowed'] = True
            self._actions_probabilities['sell']['allowed'] = True
            self._actions_probabilities['close']['allowed'] = False
        elif prev_state.parameters['buy'] or prev_state.parameters['sell']:
            self._actions_probabilities['close']['allowed'] = True
            if prev_state.parameters['buy']:
                self._actions_probabilities['buy']['allowed'] = False
            else:
                self._actions_probabilities['buy']['allowed'] = True
            if prev_state.parameters['sell']:
                self._actions_probabilities['sell']['allowed'] = False

    def init_from_prev_state(self, prev_state):
        pass


class tsZigZagPointType(Enum):
    Minimum = 0,
    Maximum = 1


class TradingState:
    def __init__(
            self,
            owner_form=None,
            symbol=None,
            ticks_history_folder=None,
            tick_date=None,
            tick_index=None,
            ticks_frame_size=8192,
            bid_ask_percents_neuroinputs_resolution=16,
            bid_ask_percents_neuroinputs_k=5000,
            bid_ask_points_neuroinputs_resolution=16,
            bid_ask_points_neuroinputs_k=0.01,
            look_forward_ticks=1024,
            ema_period=1000,
            accuracy=5
    ):
        self._owner_form = owner_form
        self._symbol = symbol
        self._ticks_history = TicksHistory(symbol=symbol, data_files_folder=ticks_history_folder, accuracy=accuracy)
        self._tick_date = tick_date
        self._tick_index = tick_index
        self._ticks_frame_size = ticks_frame_size
        self._history = {'orders': []}
        self._ticks = self.create_ticks()
        self._neuroinputs = self.create_neuroinputs()
        self._forward_ticks = self.create_ticks()
        self._bid_ask_percents_neuroinputs_resolution = bid_ask_percents_neuroinputs_resolution
        self._bid_ask_percents_neuroinputs_k = bid_ask_percents_neuroinputs_k
        self._bid_ask_points_neuroinputs_resolution = bid_ask_points_neuroinputs_resolution
        self._bid_ask_points_neuroinputs_k = bid_ask_points_neuroinputs_k
        self._look_forward_ticks = look_forward_ticks
        self._state = tsState()
        self._zigzag = self.create_zigzag()
        self._ema = self.create_ema()
        self._ema_period = ema_period
        self._accuracy = accuracy
        self.next_day_notification = None

    def create_ticks(self):
        return {
            'date': [],
            'bid': [],
            'ask': [],
            'mid': [],
            'spread': [],
            'zigzag_prev_price': [],
            'zigzag_next_price': [],
            'bid_percent': [],
            'ask_percent': [],
            'mid_percent': [],
            'spread_percent': [],
            'bid_points': [],
            'ask_points': [],
            'mid_points': [],
            'zigzag_prev_points': [],
            'zigzag_next_points': [],
            'spread_points': []
        }

    def create_neuroinputs(self):
        return {
            'date': [],
            'bid_percent': [],
            'ask_percent': [],
            'mid_percent': [],
            'spread_percent': [],
            'ema_percent': [],
            'bid_points': [],
            'ask_points': [],
            'mid_points': [],
            'spread_points': [],
            'prev_zigzag_points': [],
            'next_zigzag_points': [],
            'ema_points': []
        }
    
    #region ticks_frame_size property
    def get_ticks_frame_size(self):
        return self._ticks_frame_size

    def set_ticks_frame_size(self, frame_size):
        self._ticks_frame_size = frame_size

    ticks_frame_size = property(get_ticks_frame_size, set_ticks_frame_size)
    #endregion

    #region ticks_history property
    def get_ticks_history(self):
        return self._ticks_history

    ticks_history = property(get_ticks_history)
    #endregion

    #region tick_index property
    def get_tick_index(self):
        return self._tick_index

    def set_tick_index(self, tick_index):
        self._tick_index = tick_index

    tick_index = property(get_tick_index, set_tick_index)
    #endregion

    #region ticks property
    def get_ticks(self):
        return self._ticks

    ticks = property(get_ticks)
    #endregion

    # TODO: Write other TradingState properties implementation

    def go_to_start(self):
        self._ticks_history.go_to_start()
        self._tick_date = self._ticks_history.date
        self._tick_index = self._ticks_frame_size
        self.load_ticks()

    def set_ticks_history_position(self):
        if not self._ticks_history.is_same_day(self._tick_date):
            self._ticks_history.set_date(self._tick_date)
        self._ticks_history.tick_index = self._tick_index

    def one_hot_encode(self, resolution, value, k, zero_value=0):
        result = []
        for n in range(resolution):
            result.append(0)

        if value is None:
            return result

        k_value = value * k
        tanh_value = math.tanh(k_value)
        int_value = int(tanh_value * resolution)
        onehot_index = min(zero_value + int_value, resolution - 1)
        onehot_index = max(onehot_index, 0)
        result[onehot_index] = 1
        return result

    def calc_bid_ask_percents_neuroinput_value(self, value):
        return self.one_hot_encode(resolution=self._bid_ask_percents_neuroinputs_resolution * 2 + 1, value=value, k=self._bid_ask_percents_neuroinputs_k, zero_value=self._bid_ask_percents_neuroinputs_resolution + 1)

    def calc_bid_ask_points_neuroinput_value(self, value):
        return self.one_hot_encode(resolution=self._bid_ask_points_neuroinputs_resolution * 2 + 1, value=value, k=self._bid_ask_points_neuroinputs_k, zero_value=self._bid_ask_points_neuroinputs_resolution + 1)

    def get_backward_ticks_csv(self, ticks_count=None):
        if ticks_count is None:
            temp_ticks_count = self._ticks_frame_size + 1
        else:
            temp_ticks_count = ticks_count

        temp_ticks = self.create_ticks()
        self._ticks = self.create_ticks()

        self._neuroinputs = self.create_neuroinputs()

        self.set_ticks_history_position()

        cur_tick_index = self._tick_index
        loaded_ticks_len = 0
        while loaded_ticks_len < temp_ticks_count:
            self._ticks_history.tick_index = cur_tick_index
            temp_ticks['date'].insert(0, self._ticks_history.date)
            temp_ticks['bid'].insert(0, self._ticks_history.bid)
            temp_ticks['ask'].insert(0, self._ticks_history.ask)
            loaded_ticks_len += 1

            if cur_tick_index > 0:
                cur_tick_index -= 1
            else:
                if not self._ticks_history.go_to_prev_day():
                    break
                cur_tick_index = len(self._ticks_history) - 1

        cur_tick_index2 = 0
        for cur_tick_index in range(1, len(temp_ticks['date'])):
            self._ticks['date'].append(temp_ticks['date'][cur_tick_index])
            self._ticks['bid'].append(temp_ticks['bid'][cur_tick_index])
            self._ticks['ask'].append(temp_ticks['ask'][cur_tick_index])
            self._ticks['bid_percent'].append(temp_ticks['bid'][cur_tick_index] / temp_ticks['bid'][cur_tick_index - 1] - 1)
            self._ticks['ask_percent'].append(temp_ticks['ask'][cur_tick_index] / temp_ticks['ask'][cur_tick_index - 1] - 1)

            self._neuroinputs['date'].append(temp_ticks['date'][cur_tick_index])
            self._neuroinputs['bid_percent'].append(self.calc_bid_ask_neuroinput_value(self._ticks['bid_percent'][cur_tick_index2]))
            self._neuroinputs['ask_percent'].append(self.calc_bid_ask_neuroinput_value(self._ticks['ask_percent'][cur_tick_index2]))

            cur_tick_index2 += 1

    def get_prev_zigzag_price(self, search_params):
        if search_params['point_index'] is None:
            for cur_point_index in range(len(self._zigzag['date']) - 1, -1, -1):
                if (self._zigzag['date'][cur_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][cur_point_index] < search_params['tick_index']) or self._zigzag['date'][cur_point_index].date() < search_params['date'].date():
                    if search_params['direction'] != 0:
                        search_params['point_index'] = cur_point_index
                    return self._zigzag['price'][cur_point_index]
        else:
            cur_point_index = search_params['point_index']
            if search_params['direction'] < 0:
                if (self._zigzag['date'][cur_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][cur_point_index] >= search_params['tick_index']) or self._zigzag['date'][cur_point_index].date() > search_params['date'].date():
                    if cur_point_index > 0:
                        cur_point_index -= 1
                        search_params['point_index'] = cur_point_index
                        return self._zigzag['price'][cur_point_index]
                    return None
                return self._zigzag['price'][cur_point_index]
            elif search_params['direction'] > 0:
                if cur_point_index < len(self._zigzag['date']) - 1:
                    next_point_index = cur_point_index + 1
                    if (self._zigzag['date'][next_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][next_point_index] < search_params['tick_index']) or self._zigzag['date'][next_point_index].date() < search_params['date'].date():
                        search_params['point_index'] = next_point_index
                        return self._zigzag['price'][next_point_index]
                return self._zigzag['price'][cur_point_index]
        return None

    def get_next_zigzag_price(self, search_params):
        if search_params['point_index'] is None:
            for cur_point_index in range(len(self._zigzag['date'])):
                if (self._zigzag['date'][cur_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][cur_point_index] > search_params['tick_index']) or self._zigzag['date'][cur_point_index].date() > search_params['date'].date():
                    if search_params['direction'] != 0:
                        search_params['point_index'] = cur_point_index
                    return self._zigzag['price'][cur_point_index]
        else:
            cur_point_index = search_params['point_index']
            if search_params['direction'] < 0:
                if cur_point_index > 0:
                    prev_point_index = cur_point_index - 1
                    if (self._zigzag['date'][prev_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][prev_point_index] > search_params['tick_index']) or (self._zigzag['date'][prev_point_index].date() > search_params['date'].date()):
                        search_params['point_index'] = prev_point_index
                        return self._zigzag['price'][prev_point_index]
                return self._zigzag['price'][cur_point_index]
            elif search_params['direction'] > 0:
                if (self._zigzag['date'][cur_point_index].date() == search_params['date'].date() and self._zigzag['tick_index'][cur_point_index] > search_params['tick_index']) or (self._zigzag['date'][cur_point_index].date() > search_params['date'].date()):
                    return self._zigzag['price'][cur_point_index]
                if cur_point_index < len(self._zigzag['date']) - 1:
                    cur_point_index += 1
                    search_params['point_index'] = cur_point_index
                    return self._zigzag['price'][cur_point_index]
        return None

    def get_backward_ticks(self, ticks_count=None):
        if self._ticks_history.cur_file_ext == ".csv":
            self.get_backward_ticks_csv(ticks_count)
            return

        price_to_points_k = pow(10, self._accuracy)

        if ticks_count is None:
            temp_ticks_count = self._ticks_frame_size

        self._ticks = self.create_ticks()
        self._ema = self.create_ema()
        self._neuroinputs = self.create_neuroinputs()

        self.set_ticks_history_position()
        cur_tick_index = self._tick_index

        ticks_percents_day = self.load_ticks_percents_day()
        max_ticks_percents_day_index = len(ticks_percents_day['date']) - 1

        ticks_points_day = self.load_ticks_points_day()
        max_ticks_points_day_index = len(ticks_points_day['date']) - 1

        ema_day = self.load_ema_day()
        max_ema_day_index = len(ema_day['date']) - 1

        zigzag_next_point_search_params = {
            'direction': -1,
            'date': self._ticks_history.date,
            'tick_index': self._ticks_history.tick_index,
            'point_index': None
        }
        zigzag_prev_point_search_params = {
            'direction': -1,
            'date': self._ticks_history.date,
            'tick_index': self._ticks_history.tick_index,
            'point_index': None
        }
        loaded_ticks_len = 0
        while loaded_ticks_len < temp_ticks_count:
            self._ticks_history.tick_index = cur_tick_index
            self._ticks['date'].insert(0, self._ticks_history.date)
            self._ticks['bid'].insert(0, self._ticks_history.bid)
            self._ticks['ask'].insert(0, self._ticks_history.ask)
            self._ticks['mid'].insert(0, (self._ticks_history.ask + self._ticks_history.bid) / 2)
            self._ticks['spread'].insert(0, self._ticks_history.ask - self._ticks_history.bid)

            self._neuroinputs['date'].insert(0, self._ticks_history.date)

            if cur_tick_index <= max_ticks_percents_day_index:
                self._ticks['bid_percent'].insert(0, ticks_percents_day['bid'][cur_tick_index])
                self._ticks['ask_percent'].insert(0, ticks_percents_day['ask'][cur_tick_index])
                self._ticks['mid_percent'].insert(0, ticks_percents_day['mid'][cur_tick_index])
                self._ticks['spread_percent'].insert(0, self._ticks_history.ask / self._ticks_history.bid - 1)
                
                self._neuroinputs['bid_percent'].insert(0, self.calc_bid_ask_percents_neuroinput_value(self._ticks['bid_percent'][0]))
                self._neuroinputs['ask_percent'].insert(0, self.calc_bid_ask_percents_neuroinput_value(self._ticks['ask_percent'][0]))
            else:
                self._ticks['bid_percent'].insert(0, None)
                self._ticks['ask_percent'].insert(0, None)
                self._ticks['mid_percent'].insert(0, None)
                self._ticks['spread_percent'].insert(0, None)

                self._neuroinputs['bid_percent'].insert(0, None)
                self._neuroinputs['ask_percent'].insert(0, None)

            if cur_tick_index <= max_ticks_points_day_index:
                self._ticks['bid_points'].insert(0, ticks_points_day['bid'][cur_tick_index])
                self._ticks['ask_points'].insert(0, ticks_points_day['ask'][cur_tick_index])
                self._ticks['mid_points'].insert(0, ticks_points_day['mid'][cur_tick_index])
                self._ticks['spread_points'].insert(0, int((self._ticks_history.ask - self._ticks_history.bid) * price_to_points_k))

                self._neuroinputs['bid_points'].insert(0, self.calc_bid_ask_points_neuroinput_value(self._ticks['bid_points'][0]))
                self._neuroinputs['ask_points'].insert(0, self.calc_bid_ask_points_neuroinput_value(self._ticks['ask_points'][0]))
            else:
                self._ticks['bid_points'].insert(0, None)
                self._ticks['ask_points'].insert(0, None)
                self._ticks['mid_points'].insert(0, None)
                self._ticks['spread_points'].insert(0, None)

                self._neuroinputs['bid_points'].insert(0, None)
                self._neuroinputs['ask_points'].insert(0, None)

            zigzag_next_point_search_params['date'] = self._ticks_history.date
            zigzag_next_point_search_params['tick_index'] = self._ticks_history.tick_index
            zigzag_next_price = self.get_next_zigzag_price(zigzag_next_point_search_params)
            self._ticks['zigzag_next_price'].insert(0, zigzag_next_price)

            zigzag_prev_point_search_params['date'] = self._ticks_history.date
            zigzag_prev_point_search_params['tick_index'] = self._ticks_history.tick_index
            zigzag_prev_price = self.get_prev_zigzag_price(zigzag_prev_point_search_params)
            self._ticks['zigzag_prev_price'].insert(0, zigzag_prev_price)

            self._ema['date'].insert(0, ema_day['date'][cur_tick_index])
            self._ema['price'].insert(0, ema_day['price'][cur_tick_index])

            loaded_ticks_len += 1

            if cur_tick_index > 0:
                cur_tick_index -= 1
            else:
                if not self._ticks_history.go_to_prev_day():
                    break

                cur_tick_index = len(self._ticks_history) - 1

                ticks_percents_day = self.load_ticks_percents_day()
                max_ticks_percents_day_index = len(ticks_percents_day['date']) - 1

                ticks_points_day = self.load_ticks_points_day()
                max_ticks_points_day_index = len(ticks_points_day['date']) - 1

                ema_day = self.load_ema_day()
                max_ema_day_index = len(ema_day['date']) - 1

    def get_forward_ticks_csv(self, ticks_count=None):
        if ticks_count is None:
            ticks_count = self._look_forward_ticks

        self._forward_ticks = self.create_ticks()

        self.set_ticks_history_position()

        cur_tick_index = self._tick_index + 1
        base_bid = self._ticks_history.bid
        base_ask = self._ticks_history.ask
        max_tick_index = len(self._ticks_history) - 1
        self._ticks_history.tick_index = cur_tick_index
        loaded_ticks_len = 0
        while loaded_ticks_len < ticks_count:
            self._ticks_history.tick_index = cur_tick_index
            self._forward_ticks['date'].append(self._ticks_history.date)
            self._forward_ticks['bid'].append(self._ticks_history.bid)
            self._forward_ticks['ask'].append(self._ticks_history.ask)
            self._forward_ticks['bid_percent'].append(self._ticks_history.bid / base_bid - 1)
            self._forward_ticks['ask_percent'].append(self._ticks_history.ask / base_ask - 1)
            base_bid = self._ticks_history.bid
            base_ask = self._ticks_history.ask
            loaded_ticks_len += 1

            cur_tick_index += 1
            if cur_tick_index > max_tick_index:
                if self._ticks_history.go_to_next_day():
                    max_tick_index = len(self._ticks_history) - 1
                    cur_tick_index = 0
                else:
                    break

    def get_forward_ticks(self, ticks_count=None):
        if self._ticks_history.cur_file_ext == ".csv":
            self.get_forward_ticks_csv(ticks_count)
            return

        if ticks_count is None:
            ticks_count = self._look_forward_ticks

        self._forward_ticks = self.create_ticks()

        self.set_ticks_history_position()
        max_tick_index = len(self._ticks_history) - 1
        cur_tick_index = self._tick_index + 1

        ticks_percents_day = self.load_ticks_percents_day()
        max_ticks_percents_day_index = len(ticks_percents_day['date'])

        ticks_points_day = self.load_ticks_points_day()
        max_ticks_points_day_index = len(ticks_points_day['date'])

        ema_day = self.load_ema_day()
        max_ema_day_index = len(ema_day['date']) - 1

        self._ticks_history.tick_index = cur_tick_index

        zigzag_next_point_search_params = {
            'direction': 1,
            'date': self._ticks_history.date,
            'tick_index': self._ticks_history.tick_index,
            'point_index': None
        }
        zigzag_prev_point_search_params = {
            'direction': 1,
            'date': self._ticks_history.date,
            'tick_index': self._ticks_history.tick_index,
            'point_index': None
        }
        loaded_ticks_len = 0
        while loaded_ticks_len < ticks_count:
            self._ticks_history.tick_index = cur_tick_index
            self._forward_ticks['date'].append(self._ticks_history.date)
            self._forward_ticks['bid'].append(self._ticks_history.bid)
            self._forward_ticks['ask'].append(self._ticks_history.ask)
            self._forward_ticks['mid'].append((self._ticks_history.bid + self._ticks_history.ask) / 2)

            if cur_tick_index <= max_ticks_percents_day_index:
                self._forward_ticks['bid_percent'].append(ticks_percents_day['bid'][cur_tick_index])
                self._forward_ticks['ask_percent'].append(ticks_percents_day['ask'][cur_tick_index])
                self._forward_ticks['mid_percent'].append(ticks_percents_day['mid'][cur_tick_index])

            if cur_tick_index <= max_ticks_points_day_index:
                self._forward_ticks['bid_points'].append(ticks_points_day['bid'][cur_tick_index])
                self._forward_ticks['ask_points'].append(ticks_points_day['ask'][cur_tick_index])
                self._forward_ticks['mid_points'].append(ticks_points_day['mid'][cur_tick_index])

            zigzag_next_point_search_params['date'] = self._ticks_history.date
            zigzag_next_point_search_params['tick_index'] = self._ticks_history.tick_index
            zigzag_next_price = self.get_next_zigzag_price(zigzag_next_point_search_params)
            self._forward_ticks['zigzag_next_price'].append(zigzag_next_price)

            zigzag_prev_point_search_params['date'] = self._ticks_history.date
            zigzag_prev_point_search_params['tick_index'] = self._ticks_history.tick_index
            zigzag_prev_price = self.get_prev_zigzag_price(zigzag_prev_point_search_params)
            self._forward_ticks['zigzag_prev_price'].append(zigzag_prev_price)

            if cur_tick_index <= max_ema_day_index:
                self._ema['date'].append(ema_day['date'][cur_tick_index])
                self._ema['price'].append(ema_day['price'][cur_tick_index])

            loaded_ticks_len += 1

            cur_tick_index += 1
            if cur_tick_index > max_tick_index:
                if self._ticks_history.go_to_next_day():
                    max_tick_index = len(self._ticks_history) - 1
                    cur_tick_index = 0

                    ticks_percents_day = self.load_ticks_percents_day()
                    max_ticks_percents_day_index = len(ticks_percents_day['date'])

                    ticks_points_day = self.load_ticks_points_day()
                    max_ticks_points_day_index = len(ticks_points_day['date'])

                    ema_day = self.load_ema_day()
                    max_ema_day_index = len(ema_day['date']) - 1
                else:
                    break

    def load_ticks(self):
        self.get_backward_ticks()
        self.get_forward_ticks()

    def prepare_plot_axes(self, axes, labels_and_grid=True, background_color='white'):
        axes.cla()
        if not labels_and_grid:
            axes.spines['top'].set_visible(False)
            axes.spines['right'].set_visible(False)
            axes.spines['bottom'].set_visible(False)
            axes.spines['left'].set_visible(False)
            axes.set_facecolor(background_color)
            x_axis = axes.xaxis
            x_axis.set_visible(False)
            y_axis = axes.yaxis
            y_axis.set_visible(False)
            axes.margins(x=0, y=0)
        else:
            axes.set_facecolor(background_color)
            axes.grid(True)
            axes.margins(x=0)

    def plot_ticks_bid_ask_prices(self, axes, labels_and_grid=True, background_color='white', bid_color='blue', ask_color='red', mid_color='gray', forward_bid_color='darkblue', forward_ask_color='darkred', forward_mid_color='darkgray', zigzag_color='green', zigzag_next_price_color='cyan', zigzag_prev_price_color='darkcyan'):
        max_tick_index = len(self._ticks['date']) - 1

        self.prepare_plot_axes(axes, labels_and_grid=labels_and_grid, background_color=background_color)
        axes.set_title(label="Bid/Ask prices")

        axes.plot(self._ticks['date'], self._ticks['bid'], color=bid_color)
        axes.plot(self._ticks['date'], self._ticks['ask'], color=ask_color)
        axes.plot(self._ticks['date'], self._ticks['mid'], color=mid_color)

        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['bid'][max_tick_index], self._forward_ticks['bid'][0]], color=forward_bid_color)
        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['ask'][max_tick_index], self._forward_ticks['ask'][0]], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['bid'], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['ask'], color=forward_ask_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['mid'], color=forward_mid_color)

        axes.plot(self._zigzag['date'], self._zigzag['price'], color=zigzag_color, alpha=0.75)
        axes.plot(self._ticks['date'], self._ticks['zigzag_next_price'], color=zigzag_next_price_color, alpha=0.75)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['zigzag_next_price'], color=zigzag_next_price_color, alpha=0.75)
        axes.plot(self._ticks['date'], self._ticks['zigzag_prev_price'], color=zigzag_prev_price_color, alpha=0.75)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['zigzag_prev_price'], color=zigzag_prev_price_color, alpha=0.75)

        axes.plot(self._ema['date'], self._ema['price'], color='orange', alpha=0.75)

        axes.set_xlim([self._ticks['date'][0], self._forward_ticks['date'][len(self._forward_ticks['date']) - 1]])
        ymin = min(min(self._ticks['bid']), min(self._forward_ticks['bid']))
        ymax = max(max(self._ticks['ask']), max(self._forward_ticks['ask']))
        axes.set_ylim([ymin - (1.0 / pow(10, self._accuracy) * 10), ymax + (1.0 / pow(10, self._accuracy) * 10)])

    def plot_ticks_bid_ask_percents(self, axes, labels_and_grid=True, background_color='white', bid_color='blue', ask_color='red', forward_bid_color='darkblue', forward_ask_color='darkred'):
        self.prepare_plot_axes(axes, labels_and_grid=labels_and_grid, background_color=background_color)
        axes.set_title(label="Bid/Ask percents", pad=-6, fontdict={'fontsize': 8})
        axes.plot(self._ticks['date'], self._ticks['bid_percent'], color=bid_color, alpha=0.75)
        axes.plot(self._ticks['date'], self._ticks['ask_percent'], color=ask_color, alpha=0.75)
        max_tick_index = len(self._ticks['date']) - 1
        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['bid_percent'][max_tick_index], self._forward_ticks['bid_percent'][0]], color=forward_bid_color)
        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['ask_percent'][max_tick_index], self._forward_ticks['ask_percent'][0]], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['bid_percent'], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['ask_percent'], color=forward_ask_color)

    def plot_ticks_bid_ask_points(self, axes, labels_and_grid=True, background_color='white', bid_color='blue', ask_color='red', forward_bid_color='darkblue', forward_ask_color='darkred'):
        self.prepare_plot_axes(axes, labels_and_grid=labels_and_grid, background_color=background_color)
        axes.set_title(label="Bid/Ask points", pad=-6, fontdict={'fontsize': 8})
        axes.plot(self._ticks['date'], self._ticks['bid_points'], color=bid_color, alpha=0.75)
        axes.plot(self._ticks['date'], self._ticks['ask_points'], color=ask_color, alpha=0.75)
        max_tick_index = len(self._ticks['date']) - 1
        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['bid_points'][max_tick_index], self._forward_ticks['bid_points'][0]], color=forward_bid_color)
        axes.plot([self._ticks['date'][max_tick_index], self._forward_ticks['date'][0]], [self._ticks['ask_points'][max_tick_index], self._forward_ticks['ask_points'][0]], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['bid_points'], color=forward_bid_color)
        axes.plot(self._forward_ticks['date'], self._forward_ticks['ask_points'], color=forward_ask_color)

    def get_onehot_index(self, onehot):
        return onehot.index(max(onehot))

    def plot_ticks_bid_ask_percents_neuroinputs(self, axes, labels_and_grid=True, background_color='white', bid_color='blue', ask_color='red', forward_bid_color='darkblue', forward_ask_color='darkred'):
        dates = self._neuroinputs['date']
        forward_dates = self._forward_ticks['date']
        self.prepare_plot_axes(axes, labels_and_grid=labels_and_grid, background_color=background_color)
        axes.set_title(label="Bid/Ask percents neuroinputs", pad=-6, fontdict={'fontsize': 8})
        bid_values = []
        ask_values = []
        for tick_index in range(len(self._neuroinputs['date'])):
            bid_values.append(self.get_onehot_index(self._neuroinputs['bid_percent'][tick_index]))
            ask_values.append(self.get_onehot_index(self._neuroinputs['ask_percent'][tick_index]))
        axes.set_ylim(0, len(self._neuroinputs['bid_percent'][0]) - 1)
        start_date = dates[0]
        forward_dates_len = len(forward_dates)
        if forward_dates_len > 0:
            end_date = forward_dates[forward_dates_len - 1]
        else:
            end_date = dates[len(dates) - 1]
        axes.plot([start_date, end_date], [self._bid_ask_percents_neuroinputs_resolution + 1, self._bid_ask_percents_neuroinputs_resolution + 1], color='gray')
        axes.plot(dates, bid_values, color=bid_color, alpha=0.75)
        axes.plot(dates, ask_values, color=ask_color, alpha=0.75)
        forward_values = []
        for n in range(len(forward_dates)):
            forward_values.append(0)
        axes.plot(forward_dates, forward_values, color=forward_bid_color, alpha=0)

    def plot_ticks_bid_ask_points_neuroinputs(self, axes, labels_and_grid=True, background_color='white', bid_color='blue', ask_color='red', forward_bid_color='darkblue', forward_ask_color='darkred'):
        dates = self._neuroinputs['date']
        forward_dates = self._forward_ticks['date']
        self.prepare_plot_axes(axes, labels_and_grid=labels_and_grid, background_color=background_color)
        axes.set_title(label="Bid/Ask points neuroinputs", pad=-6, fontdict={'fontsize': 8})
        bid_values = []
        ask_values = []
        for tick_index in range(len(self._neuroinputs['date'])):
            bid_values.append(self.get_onehot_index(self._neuroinputs['bid_points'][tick_index]))
            ask_values.append(self.get_onehot_index(self._neuroinputs['ask_points'][tick_index]))
        axes.set_ylim(0, len(self._neuroinputs['bid_points'][0]) - 1)
        start_date = dates[0]
        forward_dates_len = len(forward_dates)
        if forward_dates_len > 0:
            end_date = forward_dates[forward_dates_len - 1]
        else:
            end_date = dates[len(dates) - 1]
        axes.plot([start_date, end_date], [self._bid_ask_percents_neuroinputs_resolution + 1, self._bid_ask_percents_neuroinputs_resolution + 1], color='gray')
        axes.plot(dates, bid_values, color=bid_color, alpha=0.75)
        axes.plot(dates, ask_values, color=ask_color, alpha=0.75)
        forward_values = []
        for n in range(len(forward_dates)):
            forward_values.append(0)
        axes.plot(forward_dates, forward_values, color=forward_bid_color, alpha=0)

    def jump_forward(self, ticks_count):
        self.set_ticks_history_position()
        cur_ticks_len = len(self._ticks_history)
        new_tick_index = self._tick_index + ticks_count
        if new_tick_index >= cur_ticks_len:
            if self._ticks_history.go_to_next_day():
                new_tick_index = new_tick_index - cur_ticks_len
            else:
                new_tick_index = len(self._ticks_history) - 1
            self._tick_date = self._ticks_history.date
        self._tick_index = new_tick_index
        self.load_ticks()

    def jump_backward(self, ticks_count):
        self.set_ticks_history_position()
        new_tick_index = self._tick_index - ticks_count
        if new_tick_index < 0:
            if self._ticks_history.go_to_prev_day():
                new_tick_index = len(self._ticks_history) + new_tick_index
            else:
                new_tick_index = self._ticks_frame_size
            self._tick_date = self._ticks_history.date
        self._tick_index = new_tick_index
        self.load_ticks()

    def go_to_next_day(self):
        if not self._ticks_history.go_to_next_day():
            return False
        self._tick_date = self._ticks_history.date
        self._tick_index = 0
        return True

    def call_next_day_notify(self):
        if self.next_day_notification is not None:
            self.next_day_notification(self._owner_form, self._ticks_history.date)

    def recalc_ticks(self):
        self.go_to_start()
        self.call_next_day_notify()

        while True:
            self._ticks_history.convert_day_from_csv_to_pkl()
            if not self.go_to_next_day():
                break
            self.call_next_day_notify()

    def create_ticks_percents_day(self):
        return {
            'date': [],
            'bid': [],
            'ask': [],
            'mid': []
        }

    def recalc_ticks_percents(self):
        prev_bid = None
        prev_ask = None
        prev_mid = None

        self._ticks_history.go_to_start()
        ticks_len = len(self._ticks_history)
        cur_tick_index = 0
        ticks_percents_day = self.create_ticks_percents_day()
        self.call_next_day_notify()
        while True:
            self._ticks_history.tick_index = cur_tick_index
            cur_mid = (self._ticks_history.bid + self._ticks_history.ask) / 2

            if prev_bid is not None and prev_ask is not None and prev_mid is not None:
                ticks_percents_day['date'].append(self._ticks_history.date)
                ticks_percents_day['bid'].append(self._ticks_history.bid / prev_bid - 1)
                ticks_percents_day['ask'].append(self._ticks_history.ask / prev_ask - 1)
                ticks_percents_day['mid'].append(cur_mid / prev_mid - 1)
            else:
                ticks_percents_day['date'].append(self._ticks_history.date)
                ticks_percents_day['bid'].append(None)
                ticks_percents_day['ask'].append(None)
                ticks_percents_day['mid'].append(None)

            prev_bid = self._ticks_history.bid
            prev_ask = self._ticks_history.ask
            prev_mid = cur_mid

            cur_tick_index += 1
            if cur_tick_index >= ticks_len:
                self.save_ticks_percents_day(ticks_percents_day)
                if not self._ticks_history.go_to_next_day():
                    break
                ticks_len = len(self._ticks_history)
                cur_tick_index = 0
                ticks_percents_day = self.create_ticks_percents_day()
                self.call_next_day_notify()

    def ticks_percents_data_filename(self):
        return self._ticks_history.data_files_folder + "/ticks_percents_{:4d}-{:02d}-{:02d}.pkl".format(self._ticks_history.date.year, self._ticks_history.date.month, self._ticks_history.date.day)

    def save_ticks_percents_day(self, data):
        filename = self.ticks_percents_data_filename()
        with open(filename, "wb") as file:
            _data = {
                'ticks_percents': data
            }
            pickle.dump(_data, file)
            file.close()

    def load_ticks_percents_day(self):
        filename = self.ticks_percents_data_filename()
        if not os.path.exists(filename):
            return self.create_ticks_percents_day()
        with open(filename, "rb") as file:
            data = pickle.load(file)
            file.close()
        return data['ticks_percents']
    
    def create_ticks_points_day(self):
        return {
            'date': [],
            'bid': [],
            'ask': [],
            'mid': []
        }
    
    def recalc_ticks_points(self):
        price_to_points_k = pow(10, self._accuracy)
        
        prev_bid = None
        prev_ask = None
        prev_mid = None

        self._ticks_history.go_to_start()
        ticks_len = len(self._ticks_history)
        cur_tick_index = 0
        ticks_points_day = self.create_ticks_points_day()
        self.call_next_day_notify()
        while True:
            self._ticks_history.tick_index = cur_tick_index
            cur_mid = (self._ticks_history.bid + self._ticks_history.ask) / 2

            if prev_bid is not None and prev_ask is not None and prev_mid is not None:
                ticks_points_day['date'].append(self._ticks_history.date)
                ticks_points_day['bid'].append(int((self._ticks_history.bid - prev_bid) * price_to_points_k))
                ticks_points_day['ask'].append(int((self._ticks_history.ask - prev_ask) * price_to_points_k))
                ticks_points_day['mid'].append(int((cur_mid - prev_mid) * price_to_points_k))
            else:
                ticks_points_day['date'].append(self._ticks_history.date)
                ticks_points_day['bid'].append(None)
                ticks_points_day['ask'].append(None)
                ticks_points_day['mid'].append(None)

            prev_bid = self._ticks_history.bid
            prev_ask = self._ticks_history.ask
            prev_mid = cur_mid

            cur_tick_index += 1
            if cur_tick_index >= ticks_len:
                self.save_ticks_points_day(ticks_points_day)
                if not self._ticks_history.go_to_next_day():
                    break
                ticks_len = len(self._ticks_history)
                cur_tick_index = 0
                ticks_points_day = self.create_ticks_points_day()
                self.call_next_day_notify()

    def ticks_points_data_filename(self):
        return self._ticks_history.data_files_folder + "/ticks_points_{:4d}-{:02d}-{:02d}.pkl".format(self._ticks_history.date.year, self._ticks_history.date.month, self._ticks_history.date.day)

    def save_ticks_points_day(self, data):
        filename = self.ticks_points_data_filename()
        with open(filename, "wb") as file:
            _data = {
                'ticks_points': data
            }
            pickle.dump(_data, file)
            file.close()

    def load_ticks_points_day(self):
        filename = self.ticks_points_data_filename()
        if not os.path.exists(filename):
            return self.create_ticks_points_day()
        with open(filename, "rb") as file:
            data = pickle.load(file)
            file.close()
        return data['ticks_points']

    def create_zigzag(self):
        return {
            'type': [],
            'date': [],
            'tick_index': [],
            'price': []
        }

    def recalc_zigzag(self, range_threshold):
        range_threshold_value = float(range_threshold) / math.pow(10, self._accuracy)

        self._zigzag = self.create_zigzag()

        self._ticks_history.go_to_start()
        ticks_len = len(self._ticks_history)
        cur_tick_index = 0
        self.call_next_day_notify()

        last_minimum = self._ticks_history.ask
        last_maximum = self._ticks_history.bid
        while True:
            self._ticks_history.tick_index = cur_tick_index

            zigzag_last_index = len(self._zigzag['type']) - 1
            if last_minimum > self._ticks_history.ask:
                last_minimum = self._ticks_history.ask
                if zigzag_last_index >= 0 and self._zigzag['type'][zigzag_last_index] == tsZigZagPointType.Minimum:
                    self._zigzag['date'][zigzag_last_index] = self._ticks_history.date
                    self._zigzag['tick_index'][zigzag_last_index] = self._ticks_history.tick_index
                    self._zigzag['price'][zigzag_last_index] = self._ticks_history.ask
                    last_maximum = self._ticks_history.bid
                elif last_maximum - last_minimum >= range_threshold_value:
                    if zigzag_last_index < 0 or self._zigzag['type'][zigzag_last_index] == tsZigZagPointType.Maximum:
                        self._zigzag['type'].append(tsZigZagPointType.Minimum)
                        self._zigzag['date'].append(self._ticks_history.date)
                        self._zigzag['tick_index'].append(self._ticks_history.tick_index)
                        self._zigzag['price'].append(self._ticks_history.ask)
                        last_maximum = self._ticks_history.bid
            elif last_maximum < self._ticks_history.bid:
                last_maximum = self._ticks_history.bid
                if zigzag_last_index >= 0 and self._zigzag['type'][zigzag_last_index] == tsZigZagPointType.Maximum:
                    self._zigzag['date'][zigzag_last_index] = self._ticks_history.date
                    self._zigzag['tick_index'][zigzag_last_index] = self._ticks_history.tick_index
                    self._zigzag['price'][zigzag_last_index] = self._ticks_history.bid
                    last_minimum = self._ticks_history.ask
                elif last_maximum - last_minimum >= range_threshold_value:
                    if zigzag_last_index < 0 or self._zigzag['type'][zigzag_last_index] == tsZigZagPointType.Minimum:
                        self._zigzag['type'].append(tsZigZagPointType.Maximum)
                        self._zigzag['date'].append(self._ticks_history.date)
                        self._zigzag['tick_index'].append(self._ticks_history.tick_index)
                        self._zigzag['price'].append(self._ticks_history.bid)
                        last_minimum = self._ticks_history.ask

            cur_tick_index += 1
            if cur_tick_index >= ticks_len:
                if not self._ticks_history.go_to_next_day():
                    break
                ticks_len = len(self._ticks_history)
                cur_tick_index = 0
                self.call_next_day_notify()

        self.save_zigzag(filename_postfix="{:d}".format(range_threshold))

    def save_zigzag(self, filename_postfix):
        filename = self._ticks_history.data_files_folder + "/zigzag_" + filename_postfix + ".pkl"
        with open(filename, "wb") as file:
            data = {
                'zigzag': self._zigzag
            }
            pickle.dump(data, file)
            file.close()
    
    def load_zigzag(self, filename_postfix):
        filename = self._ticks_history.data_files_folder + "/zigzag_" + filename_postfix + ".pkl"
        with open(filename, "rb") as file:
            data = pickle.load(file)
            self._zigzag = data['zigzag']
            file.close()

    def create_ema(self):
        return {
            'date': [],
            'price': []
        }

    def recalc_ema(self):
        k = 2 / (self._ema_period + 1)

        self._ticks_history.go_to_start()
        ticks_len = len(self._ticks_history)
        cur_tick_index = 0
        self.call_next_day_notify()

        ema_day = self.create_ema()
        prev_ema = None
        while True:
            self._ticks_history.tick_index = cur_tick_index
            mid_price = (self._ticks_history.bid + self.ticks_history.ask) / 2

            if prev_ema is not None:
                ema = (mid_price * k) + (prev_ema * (1 - k))
            else:
                ema = mid_price

            ema_day['date'].append(self._ticks_history.date)
            ema_day['price'].append(ema)

            prev_ema = ema

            cur_tick_index += 1
            if cur_tick_index >= ticks_len:
                self.save_ema_day(ema_day, "{}".format(self._ema_period))

                if not self._ticks_history.go_to_next_day():
                    break
                ticks_len = len(self._ticks_history)
                cur_tick_index = 0
                ema_day = self.create_ema()
                self.call_next_day_notify()

    def get_ema_filename(self, filename_postfix):
        return self._ticks_history.data_files_folder + "/ema_" + filename_postfix + "_{:4d}-{:02d}-{:02d}.pkl".format(self._ticks_history.date.year, self._ticks_history.date.month, self._ticks_history.date.day)

    def save_ema_day(self, ema, filename_postfix):
        filename = self.get_ema_filename(filename_postfix)
        with open(filename, "wb") as file:
            data = {
                'ema': ema
            }
            pickle.dump(data, file)
            file.close()

    def load_ema_day(self, filename_postfix=None):
        if filename_postfix is None:
            filename_postfix = "{}".format(self._ema_period)
        filename = self.get_ema_filename(filename_postfix)
        if not os.path.exists(filename):
            return self.create_ema()
        with open(filename, "rb") as file:
            data = pickle.load(file)
            file.close()
        return data['ema']
