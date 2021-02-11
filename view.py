from PyQt5.QtWidgets import *
import PyQt5.QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import controller as c

parameters = {"Stock to trade": 1,
              "Upper Market Variation Limit": 0.022,
              "Lower Market Variation Limit": -0.018,
              "Entry Price (EP)": 100,
              "Trading rounds": 15,
              "Buffer size": 12,
              "c_factor": 1.5,
              "Model (1 for lin, 2 for quad)": 2,
              "Refresh rate (s)" : 1}
parameters_lines = {}

class Window(QDialog):
    global parameters, parameters_lines

    def __init__(self):
        super().__init__()

        self.title = "Automatic Day Trader"
        self.left = 0
        self.top = 0
        self.width = 1440
        self.height = 810

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.InitUI()
        self.showMaximized()
        self.show()

    def InitUI(self):
        main_window = self.make_window()

    def make_window(self):
        mainBox = QVBoxLayout()
        self.setLayout(mainBox)

        paraVBox = self.set_parameters_vbox()

        self.marketGraph = MplWidget()
        self.marketGraphTB = NavigationToolbar(self.marketGraph.canvas, self)
        market_graph_vBox = QVBoxLayout()
        market_graph_vBox.addWidget(self.marketGraph)
        market_graph_vBox.addWidget(self.marketGraphTB)
        self.strategyGraph = MplWidget()
        self.strategyGraphTB = NavigationToolbar(self.strategyGraph.canvas, self)
        strategy_graph_vBox = QVBoxLayout()
        strategy_graph_vBox.addWidget(self.strategyGraph)
        strategy_graph_vBox.addWidget(self.strategyGraphTB)
        self.ratesGraph = MplWidget()
        self.ratesGraphTB = NavigationToolbar(self.ratesGraph.canvas, self)
        rates_graph_vBox = QVBoxLayout()
        rates_graph_vBox.addWidget(self.ratesGraph)
        rates_graph_vBox.addWidget(self.ratesGraphTB)
        self.buyPowerGraph = MplWidget()
        self.buyPowerGraphTB = NavigationToolbar(self.buyPowerGraph.canvas, self)
        buyPower_graph_vBox = QVBoxLayout()
        buyPower_graph_vBox.addWidget(self.buyPowerGraph)
        buyPower_graph_vBox.addWidget(self.buyPowerGraphTB)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        radioButtonHBox = QHBoxLayout()
        self.simRadioButton = QRadioButton('Full Simulation')
        self.simRadioButton.setChecked(True)
        self.realRadioButton = QRadioButton('Real Price Simulation')
        self.rhRadioButton = QRadioButton('Robinhood')
        radioButtonHBox.addWidget(self.simRadioButton)
        radioButtonHBox.addWidget(self.realRadioButton)
        radioButtonHBox.addWidget(self.rhRadioButton)

        self.dayTradeButton = QPushButton('Run!')
        self.dayTradeButton.clicked.connect((self.run))
        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stop)

        paraVBox.addLayout(radioButtonHBox)
        paraVBox.addWidget((self.dayTradeButton))
        paraVBox.addWidget(self.stopButton)

        topHBox = QHBoxLayout()
        topHBox.addLayout(paraVBox)
        topHBox.addLayout(strategy_graph_vBox)
        topHBox.addLayout(rates_graph_vBox)

        botHBox = QHBoxLayout()
        botHBox.addWidget(self.log)
        botHBox.addLayout(market_graph_vBox)
        botHBox.addLayout(buyPower_graph_vBox)

        mainBox.addLayout(topHBox)
        mainBox.addLayout(botHBox)
        return mainBox

    def set_parameters_vbox(self):
        self.pVBox = QVBoxLayout()
        for key in parameters:
            hBox = QHBoxLayout()
            self.line = QLineEdit(key)
            self.line.setText(str(parameters[key]))
            parameters_lines[key] = self.line
            label = QLabel()
            label.setText(key + ":")
            hBox.addWidget(label)
            hBox.addWidget(self.line)
            self.pVBox.addLayout(hBox)
        return self.pVBox

    def run(self):
        c.run(self)

    def stop(self):
        c.stop(self)

    def clear_graphs(self):
        graphs = [self.marketGraph, self.ratesGraph, self.strategyGraph, self.buyPowerGraph]
        for graph in graphs:
            graph.canvas.axes.clear()
            graph.canvas.draw()

    def log(self, text):
        self.log.append(text)

    def plot(self, data, graph, graph_type, title, x_label, y_label):
        graph.canvas.axes.clear()
        graph.canvas.axes.set_title(title)
        graph.canvas.axes.set_xlabel(x_label)
        graph.canvas.axes.set_ylabel(y_label)
        if graph_type == 1:
            for key in data:
                graph.canvas.axes.data(*zip(*sorted(data[key].items())), label=key)
        elif graph_type == 2:
            data.plot(y=['r', 'r_a', 'r_u', 'r_l'], ax=graph.canvas.axes)
        elif graph_type == 3:
            data.plot(y=['h', 'T', 'i_s'], ax=graph.canvas.axes)
        elif graph_type == 4:
            data.plot(y=['CP', 'CP_avg'], ax=graph.canvas.axes)
        graph.canvas.draw()

    def get_parameters(self):
        for key in parameters:
            parameters[key] = float(parameters_lines.get(key).text())
        return parameters


class MplWidget(PyQt5.QtWidgets.QWidget):

    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = PyQt5.QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

