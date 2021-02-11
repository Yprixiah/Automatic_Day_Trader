import PyQt5.QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


class MplWidget(PyQt5.QtWidgets.QWidget):

    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = PyQt5.QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
