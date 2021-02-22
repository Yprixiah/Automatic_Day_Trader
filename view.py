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
trading_type = 'fs'
credentials = []

class Window(QDialog):
    global parameters, parameters_lines

    def __init__(self):
        super().__init__()

        self.width = 1440
        self.height = 810

        self.setWindowTitle("Automatic Day Trader")
        self.setGeometry(0, 0, self.width, self.height)

        self.InitUI()
        self.showMaximized()
        self.show()

    def InitUI(self):
        main_window = self.make_window()

    def make_window(self):
        mainBox = QVBoxLayout()
        self.setLayout(mainBox)

        paraVBox = self.set_parameters_vbox()

        self.valueGraph = MplWidget()
        self.valueGraphTB = NavigationToolbar(self.valueGraph.canvas, self)
        value_graph_vBox = QVBoxLayout()
        value_graph_vBox.addWidget(self.valueGraph)
        value_graph_vBox.addWidget(self.valueGraphTB)
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
        self.marketGraph = MplWidget()
        self.marketGraphTB = NavigationToolbar(self.marketGraph.canvas, self)
        market_graph_vBox = QVBoxLayout()
        market_graph_vBox.addWidget(self.marketGraph)
        market_graph_vBox.addWidget(self.marketGraphTB)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        radioButtonHBox = QHBoxLayout()
        self.simRadioButton = QRadioButton('Full Simulation')
        self.simRadioButton.setChecked(True)
        self.simRadioButton.clicked.connect(self.set_credentials)
        self.realRadioButton = QRadioButton('Real Price Simulation')
        self.realRadioButton.clicked.connect(self.set_credentials)
        self.rhRadioButton = QRadioButton('Robinhood')
        self.rhRadioButton.clicked.connect(self.set_credentials)
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
        botHBox.addLayout(value_graph_vBox)
        botHBox.addLayout(market_graph_vBox)

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
            label.setText(key + ": ")
            hBox.addWidget(label)
            hBox.addWidget(self.line)
            self.pVBox.addLayout(hBox)
        return self.pVBox

    def run(self):
        c.run(self)

    def stop(self):
        c.stop(self)

    def clear_graphs(self):
        graphs = [self.valueGraph, self.ratesGraph, self.strategyGraph, self.marketGraph]
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
            data.plot(y=['MP'], ax=graph.canvas.axes)
        elif graph_type == 2:
            data.plot(y=['r', 'r_a', 'r_u', 'r_l'], ax=graph.canvas.axes)
        elif graph_type == 3:
            data.plot(y=['h', 'T', 'i_s'], ax=graph.canvas.axes)
        elif graph_type == 4:
            data.plot(y=['VP', 'VP_avg'], ax=graph.canvas.axes)
        graph.canvas.draw()

    def get_parameters(self):
        for key in parameters:
            parameters[key] = float(parameters_lines.get(key).text())
        return parameters

    def set_credentials(self):
        global credentials, trading_type
        if self.simRadioButton.isChecked() == True:
            credentials = []
            trading_type = 'fs'
        elif self.realRadioButton.isChecked() == True:
            c.prompt_login(self)
            trading_type = 'rs'
        elif self.rhRadioButton.isChecked() == True:
            c.prompt_login(self)
            trading_type = 'rh'

    def get_credentials(self):
        return credentials

    def get_trading_type(self):
        return trading_type


class MplWidget(PyQt5.QtWidgets.QWidget):

    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = PyQt5.QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


class login_window(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Robinhood Login')
        self.setGeometry(400, 400, 400, 200)

        self.InitUI()
        self.show()

    def InitUI(self):
        mainVBox = QVBoxLayout()
        self.setLayout(mainVBox)

        topHBox = QHBoxLayout()
        lowHBox = QHBoxLayout()

        loginLabel = QLabel()
        loginLabel.setText('Login: ')
        self.loginLine = QLineEdit()
        topHBox.addWidget(loginLabel)
        topHBox.addWidget(self.loginLine)

        passLabel = QLabel()
        passLabel.setText('Password: ')
        self.passLine = QLineEdit()
        lowHBox.addWidget(passLabel)
        lowHBox.addWidget(self.passLine)

        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.validate)

        mainVBox.addLayout(topHBox)
        mainVBox.addLayout(lowHBox)
        mainVBox.addWidget(self.okButton)

    def validate(self):
        global credentials
        credentials = [self.loginLine.text(), self.passLine.text()]
        c.rh_login(self)
        self.close()
        return credentials
