from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# plots the canvas on which we can draw graphs
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def set_xlabel(self, x_label):
        self.axes.set_xlabel(x_label)

    def set_ylabel(self, y_label):
        self.axes.set_ylabel(y_label)

    def set_label(self, label):
        self.axes.set_title(label)

    def set_grid(self):
        self.axes.grid(True)

    def delete_grid(self):
        self.axes.grid(False)