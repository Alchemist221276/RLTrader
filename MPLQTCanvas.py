from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib import pyplot as plt
from PySide6.QtWidgets import QSizePolicy


class MPLQTCanvas(FigureCanvasQTAgg):
    def __init__(self, figure=None, parent=None):
        super().__init__(figure)
        #super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

