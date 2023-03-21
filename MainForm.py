from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import QSize
from MPLQTCanvas import MPLQTCanvas
from TradingState import TradingState
from ui.MainFormUI import Ui_MainForm


def ticks_history_recalc_ticks_next_day_notify(main_form, new_date):
    main_form.set_statusbar_text("Calculating ticks {:02d}.{:02d}.{:4d}...".format(new_date.day, new_date.month, new_date.year))


def ticks_history_recalc_ticks_percents_next_day_notify(main_form, new_date):
    main_form.set_statusbar_text("Calculating ticks percents {:02d}.{:02d}.{:4d}...".format(new_date.day, new_date.month, new_date.year))


def ticks_history_recalc_ticks_points_next_day_notify(main_form, new_date):
    main_form.set_statusbar_text("Calculating ticks points {:02d}.{:02d}.{:4d}...".format(new_date.day, new_date.month, new_date.year))


def ticks_history_recalc_zigzag_next_day_notify(main_form, new_date):
    main_form.set_statusbar_text("Calculating ZigZag {:02d}.{:02d}.{:4d}...".format(new_date.day, new_date.month, new_date.year))


def ticks_history_recalc_ema_next_day_notify(main_form, new_date):
    main_form.set_statusbar_text("Calculating EMA {:02d}.{:02d}.{:4d}...".format(new_date.day, new_date.month, new_date.year))


class MainForm(QMainWindow):
    def __init__(self, application=None):
        super().__init__()

        self._application = application
        self._page_scroll_amount = 500

        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        #region Status bar initialization
        self.ui.statusbarText = QLabel()
        self.ui.statusbar.addPermanentWidget(self.ui.statusbarText, stretch=100)
        #endregion Status bar initialization

        #region Connect actions
        self.ui.actionExit.triggered.connect(self.execute_exit_action)
        self.ui.actionRecalculate_ticks.triggered.connect(self.execute_Recalculate_ticks_action)
        self.ui.actionRecalculate_ticks_percents.triggered.connect(self.execute_Recalculate_ticks_percents_action)
        self.ui.actionRecalculate_ticks_points.triggered.connect(self.execute_Recalculate_ticks_points_action)
        self.ui.actionRecalculate_zigzag.triggered.connect(self.execute_Recalculate_zigzag_action)
        self.ui.actionRecalculate_EMA.triggered.connect(self.execute_Recalculate_EMA_action)

        self.ui.PageUpButton.clicked.connect(self.PageUpButton_click)
        self.ui.PageDnButton.clicked.connect(self.PageDnButton_click)
        #endregion Connect actions

        #region Charts canvases initialization
        self.ui.ticks_frame_prices_chart_canvas = MPLQTCanvas()
        self.ui.ticks_frame_chart_layout.addWidget(self.ui.ticks_frame_prices_chart_canvas)

        self.ui.ticks_frame_bid_ask_percents_canvas = MPLQTCanvas()
        self.ui.ticks_frame_bid_ask_percents_canvas.setMaximumSize(QSize(16777215, 100))
        self.ui.ticks_frame_chart_layout.addWidget(self.ui.ticks_frame_bid_ask_percents_canvas)

        self.ui.ticks_frame_bid_ask_neuroinputs = MPLQTCanvas()
        self.ui.ticks_frame_bid_ask_neuroinputs.setMaximumSize(QSize(16777215, 100))
        self.ui.ticks_frame_chart_layout.addWidget(self.ui.ticks_frame_bid_ask_neuroinputs)
        #endregion Charts canvases initialization

        #region Trading state initialization
        self.trading_state = TradingState(owner_form=self, symbol="EURUSDrfd", ticks_history_folder="history\AlfaForex\EURUSDrfd")
        self.trading_state.load_zigzag(filename_postfix="100")
        self.trading_state.go_to_start()
        #TODO: Provide for a situation when the ticks in the day are smaller than the frame size
        self.trading_state.tick_index = self.trading_state.ticks_frame_size
        #endregion Trading state initialization

        self.update_canvases()

    def set_statusbar_text(self, text):
        self.ui.statusbarText.setText(text)
        self.ui.statusbarText.repaint()
        if self._application is not None:
            self._application.processEvents()

    def clear_status_bar(self):
        self.set_statusbar_text("")

    def update_ticks_frame_prices_chart_canvas(self):
        canvas = self.ui.ticks_frame_prices_chart_canvas
        figure = canvas.figure
        axes = figure.gca()
        self.trading_state.plot_ticks_bid_ask_prices(axes=axes, labels_and_grid=True)
        canvas.draw()

    def update_ticks_frame_percents_chart_canvas(self):
        canvas = self.ui.ticks_frame_bid_ask_percents_canvas
        self.trading_state.plot_ticks_bid_ask_percents(axes=canvas.figure.gca(), labels_and_grid=True)
        canvas.draw()

    def update_ticks_frame_bid_ask_neuroinputs_chart_canvas(self):
        canvas = self.ui.ticks_frame_bid_ask_neuroinputs
        self.trading_state.plot_ticks_bid_ask_neuroinputs(axes=canvas.figure.gca(), labels_and_grid=True)
        canvas.draw()

    def update_canvases(self):
        self.update_ticks_frame_prices_chart_canvas()
        self.update_ticks_frame_percents_chart_canvas()
        self.update_ticks_frame_bid_ask_neuroinputs_chart_canvas()

    def ticks_frame_pageup(self):
        self.trading_state.jump_forward(self._page_scroll_amount)

    def ticks_frame_pagedn(self):
        self.trading_state.jump_backward(self._page_scroll_amount)

    def PageUpButton_click(self):
        self.ticks_frame_pageup()
        self.update_canvases()

    def PageDnButton_click(self):
        self.ticks_frame_pagedn()
        self.update_canvases()

    def execute_exit_action(self):
        self.close()

    def execute_Recalculate_ticks_action(self):
        if self.trading_state._ticks_history.data_files_format() != ".csv":
            print("Ticks history data files format is allready pkl")
            return
        self.trading_state.next_day_notification = ticks_history_recalc_ticks_next_day_notify
        self.trading_state.recalc_ticks()
        self.clear_status_bar()

    def execute_Recalculate_ticks_percents_action(self):
        self.trading_state.next_day_notification = ticks_history_recalc_ticks_percents_next_day_notify
        self.trading_state.recalc_ticks_percents()
        self.clear_status_bar()

    def execute_Recalculate_ticks_points_action(self):
        self.trading_state.next_day_notification = ticks_history_recalc_ticks_points_next_day_notify
        self.trading_state.recalc_ticks_points()
        self.clear_status_bar()

    def execute_Recalculate_zigzag_action(self):
        self.trading_state.next_day_notification = ticks_history_recalc_zigzag_next_day_notify
        #TODO: Replace hardcode params in MainForm.execute_Recalculate_zigzag_action()
        self.trading_state.recalc_zigzag(100)
        self.update_ticks_frame_prices_chart_canvas()
        self.clear_status_bar()

    def execute_Recalculate_EMA_action(self):
        self.trading_state.next_day_notification = ticks_history_recalc_ema_next_day_notify
        self.trading_state.recalc_ema()
        self.update_ticks_frame_prices_chart_canvas()
        self.clear_status_bar()
