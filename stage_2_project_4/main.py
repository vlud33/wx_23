import sys 
import data_filter
import ReceiveDummyData
import numpy as np
from Canvas import MplCanvas
from MQTT import MQTTClient
from DrawGraphs import *

import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from matplotlib.figure import Figure
import loss_finder
import peak_finder


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainUI(QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        self.ui = uic.loadUi("main.ui", self)
        self.time_interval = int(self.ui.lineEdit.text())
        self.ui.lineEdit.textChanged.connect(self.timeIntervalChanged)

        self.canvas1 = MplCanvas(self)
        self.canvas2 = MplCanvas(self)

        self.toolbar1 = NavigationToolbar2QT(self.canvas1, self)
        self.toolbar2 = NavigationToolbar2QT(self.canvas2, self)

        self.set_canvas_labels()
        self.add_widgets()

        self.data_filter = data_filter.DataFilter()

        self.graph1 = DrawGraph()
        self.graph2 = DrawGraph()
        self.graph3 = DrawGraph()

        # self.R5IM = []
        # r5im_data = ReceiveDummyData.get_r5im(3)

        # self.blm = []
        # blm_data = ReceiveDummyData.get_blm(3, 39)

        self.client = MQTTClient("ac_phys/workxp/live_signals")
        self.client.connect("130.246.57.45", 8883, 60)
        self.client.loop_start()

        # for i in range(3):
        #     self.R5IM.append(r5im_data[i] * -1)
            
        # for i in range (3):
        #     minimum = min(blm_data[i])
        #     self.blm.append(blm_data[i]-minimum)

        self.xdata = np.linspace(-0.5, 10.5, 2200)

        self.draw_data()

        self.repeater()

    # if freqyency changed 
    def timeIntervalChanged(self):
        try:
            a = int(self.ui.lineEdit.text())
        
        except ValueError:
            return
                
        self.time_interval = int(self.ui.lineEdit.text())

    # when program closed
    def closeEvent(self, a0):
        #for live data
        self.client.loop_stop()
        self.client.disconnect()
        
        return super().closeEvent(a0)

    def add_widgets(self):
        self.gridLayout.addWidget(self.canvas2)
        self.gridLayout.addWidget(self.toolbar2)
        self.gridLayout_2.addWidget(self.toolbar1)
        self.gridLayout_2.addWidget(self.canvas1)

    def get_live_data(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.client.connect("130.246.57.45", 8883, 60)
        self.client.loop_start()

    def set_canvas_labels(self):
        self.canvas1.set_xlabel("Time [ms]")
        self.canvas1.set_ylabel("Volts [V]")
        self.canvas1.set_label("BLM Sum")
        self.canvas1.set_grid()
        self.canvas2.set_label("R5IM")
        self.canvas2.set_ylabel("Volts [V]")
        self.canvas2.set_xlabel("Time [ms]")
        self.canvas2.set_grid()

    # draw graph every self.time_interval
    def repeater(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.time_interval)
        # for live data
        self.timer.timeout.connect(self.get_live_data)
        self.timer.timeout.connect(self.draw_data)
        self.timer.start()

    def draw_data(self):
        # for demo
        # self.graph1.draw(self.canvas1, self.xdata, self.blm, False) #False: don't draw bars
        # self.graph2.draw(self.canvas2, self.xdata, self.R5IM, True) #True: draw bars

        data = None
        data = self.client.get_data()
        
        # if data is None(we haven't received it yet) then do nothing
        if data is None:
            return
        
        x, gradient = self.get_gradient(self.data_filter.filter_r5im(data[39]))
        self.graph1.draw(self.canvas1, self.xdata, np.sum(self.data_filter.filter_blm(data[1:38]), axis=0), False, True)
        self.graph2.draw(self.canvas2, self.xdata, self.data_filter.filter_r5im(data[39]), True, False)
        self.graph3.draw(self.canvas1, x, gradient, False, False)

        # for every data
        self.canvas1.draw()
        self.canvas2.draw()

    def get_gradient(self, r5im):
               
        array = []
        for i in range (0,len(r5im), 10):
            array.append(r5im[i])
        grad = np.gradient(array)

        x = np.linspace(-0.5,10.5,len(array))

        return x, grad 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
