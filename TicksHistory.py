from datetime import datetime, timedelta
import os
import MetaTrader5 as Mt5
import pandas as pd
import pickle


class TicksHistory:
    def __init__(self, symbol, data_files_folder=None, accuracy=5):
        self._symbol = symbol
        self._data_files_folder = data_files_folder
        self._cur_filename = None
        self._accuracy = accuracy
        self._ticks = None
        self._tick_index = None

    def __len__(self):
        return len(self._ticks['date'])

    def get_full_filename(self, filename):
        return "{}/{}".format(self._data_files_folder, filename)

    def get_filename_datetime_date_str(self, date):
        return "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day)

    def get_filename_from_date(self, date):
        file_ext = ""
        files_list = self.get_ticks_files_list()
        if len(files_list) > 0:
            file_ext = os.path.splitext(files_list[0])[1]
        return str.format("{}/Ticks_{}_{}{}", self._data_files_folder, self._symbol, self.get_filename_datetime_date_str(date), file_ext)

    def get_ticks_files_list(self):
        filename_prefix = "ticks_" + self._symbol.lower() + "_"
        #files_list = [_ for _ in os.listdir(self._data_files_folder) if _.lower().startswith(filename_prefix) and _.endswith(".csv")]
        files_list = [_ for _ in os.listdir(self._data_files_folder) if _.lower().startswith(filename_prefix) and _.lower().endswith(".pkl")]
        if len(files_list) == 0:
            return []
        files_list.sort()
        return files_list

    def get_day_from_mt5(self, date):
        if not Mt5.initialize():
            Mt5.shutdown()
            raise RuntimeError("mt5 initialize failed")
        mt5_ticks = Mt5.copy_ticks_range(
            self._symbol,
            datetime(date.year, date.month, date.day),
            datetime(date.year, date.month, date.day, 23, 59, 59),
            Mt5.COPY_TICKS_ALL
        )
        Mt5.shutdown()

        if len(mt5_ticks) == 0:
            return False

        ticks = []
        for mt5_tick in mt5_ticks:
            ticks.append([datetime.fromtimestamp(mt5_tick[0]), mt5_tick[1], mt5_tick[2]])
        with open(self.get_filename_from_date(date) + ".pkl", 'wb') as file:
            data = {
                'ticks': ticks
            }
            pickle.dump(data, file)
            file.close()
        print("Updated ticks from MT5: Symbol={}, Date={:02}.{:02d}.{:04d}".format(self._symbol, date.day, date.month, date.year))

        return True

    def get_days_from_mt5(self, start_date, end_date):
        cur_date = datetime(start_date.year, start_date.month, start_date.day)
        while cur_date < end_date:
            self.get_day_from_mt5(cur_date)
            cur_date += timedelta(days=1)

    def load_cur_file(self):
        cur_file_ext = self.cur_file_ext
        if cur_file_ext == ".pkl":
            with open(self._cur_filename, "rb") as file:
                data = pickle.load(file)
                self._ticks = data['ticks']
                file.close()
        elif cur_file_ext == ".csv":
            self._ticks = pd.read_csv(self._cur_filename)
        self._tick_index = 0

    def load_day(self, date):
        self._cur_filename = self.get_filename_from_date(date)
        self.load_cur_file()

    def go_to_start(self):
        if self._data_files_folder is None:
            raise RuntimeError("_cur_filename is not initialized")

        files_list = self.get_ticks_files_list()
        if len(files_list) == 0:
            raise RuntimeError("No files in _data_files_folder")
        self.cur_filename = self.get_full_filename(files_list[0])

        return True

    #region data_files_folder property
    def get_data_files_folder(self):
        return self._data_files_folder

    data_files_folder = property(get_data_files_folder)
    #endregion data_files_folder property

    #region date property
    def get_date(self):
        if self._ticks is None:
            raise RuntimeError("_ticks is not initialized")
        cur_file_ext = self.cur_file_ext
        if cur_file_ext == ".csv":
            return datetime.strptime(self._ticks['date'][self._tick_index], "%Y-%m-%d %H:%M:%S")
        elif cur_file_ext == ".pkl":
            return self._ticks['date'][self._tick_index]

    def set_date(self, date):
        self.load_day(date)

    date = property(get_date, set_date)
    #endregion date property

    #region bid property
    def get_bid(self):
        if self._ticks is None:
            raise RuntimeError("_ticks is not initialized")
        return self._ticks['bid'][self._tick_index]

    bid = property(get_bid)
    #endregion bid property

    #region ask property
    def get_ask(self):
        if self._ticks is None:
            raise RuntimeError("_ticks is not initialized")
        return self._ticks['ask'][self._tick_index]

    ask = property(get_ask)
    #endregion ask property
    
    #region symbol property
    def get_symbol(self):
        return self._symbol

    symbol = property(get_symbol)
    #endregion symbol property

    #region ticks property
    def get_ticks(self):
        return self._ticks

    ticks = property(get_ticks)
    #endregion ticks property
    
    #region tick_index property
    def get_tick_index(self):
        return self._tick_index

    def set_tick_index(self, tick_index):
        if tick_index >= len(self._ticks['date']):
            raise ValueError("tick_index is out of range")
        self._tick_index = tick_index

    tick_index = property(get_tick_index, set_tick_index)
    #endregion ticks_index property

    #region cur_file_ext property
    def get_cur_file_ext(self):
        return os.path.splitext(self._cur_filename)[1]

    cur_file_ext = property(get_cur_file_ext)
    #endregion cur_file_ext property

    #region cur_filename property
    def get_cur_filename(self):
        return self._cur_filename

    def set_cur_filename(self, filename):
        self._cur_filename = filename
        self.load_cur_file()

    cur_filename = property(get_cur_filename, set_cur_filename)
    #endregion cur_filename property

    #region accuracy property
    def get_accuracy(self):
        return self._accuracy

    def set_accuracy(self, value):
        self._accuracy = value

    accuracy = property(get_accuracy, set_accuracy)
    #endregion accuracy property

    def go_to_prev_day(self):
        files_list = self.get_ticks_files_list()
        cur_file_index = files_list.index(os.path.basename(self._cur_filename))
        if cur_file_index == 0:
            return False
        self.cur_filename = self.get_full_filename(files_list[cur_file_index - 1])
        return True

    def go_to_next_day(self):
        files_list = self.get_ticks_files_list()
        cur_file_index = files_list.index(os.path.basename(self._cur_filename))
        if cur_file_index >= len(files_list) - 1:
            return False
        self.cur_filename = self.get_full_filename(files_list[cur_file_index + 1])
        return True

    def data_files_format(self):
        files_list = self.get_ticks_files_list()
        if len(files_list) == 0:
            return None
        file_ext = os.path.splitext(files_list[0])[1]
        if file_ext == ".csv" or file_ext == ".pkl":
            return file_ext
        raise RuntimeError("Unknown data file extention")

    def is_same_day(self, date):
        if self.date.day == date.day and self.date.month == date.month and self.date.year == date.year:
            return True
        return False

    def convert_day_from_csv_to_pkl(self):
        ticks_len = len(self._ticks['date'])
        new_ticks = {
            'date': [None] * ticks_len,
            'bid': [None] * ticks_len,
            'ask': [None] * ticks_len
        }

        for cur_tick_index in range(ticks_len):
            new_ticks['date'][cur_tick_index] = datetime.strptime(self._ticks['date'][cur_tick_index], "%Y-%m-%d %H:%M:%S")
            new_ticks['bid'][cur_tick_index] = self._ticks['bid'][cur_tick_index]
            new_ticks['ask'][cur_tick_index] = self._ticks['ask'][cur_tick_index]

        self._ticks = new_ticks
        self.save_day()

    def save_day(self):
        with open(os.path.splitext(self._cur_filename)[0] + ".pkl", "wb") as file:
            data = {
                'ticks': self._ticks
            }
            pickle.dump(data, file)
            file.close()
