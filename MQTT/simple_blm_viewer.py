import sys
import numpy as np
import multiprocessing
import paho.mqtt.client as mqtt
from PyQt5.QtGui import * 
import PyQt5.QtWidgets as qt
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt5 import QtCore, QtGui, QtWidgets


r0_patch = mpatches.Patch(color='blue', label='R0')
r1_patch = mpatches.Patch(color='darkviolet', label='R1')
r2_patch = mpatches.Patch(color='deeppink', label='R2')
r3_patch = mpatches.Patch(color='crimson', label='R3')
r4_patch = mpatches.Patch(color='coral', label='R4')
r5_patch = mpatches.Patch(color='gold', label='R5')
r6_patch = mpatches.Patch(color='lime', label='R6')
r7_patch = mpatches.Patch(color='forestgreen', label='R7')
r8_patch = mpatches.Patch(color='turquoise', label='R8')
r9_patch = mpatches.Patch(color='cornflowerblue', label='R9')
im_patch = mpatches.Patch(color='navy', label='R5IM')
sum_patch = mpatches.Patch(color='black', label='SUM')
sum2_patch = mpatches.Patch(color='gray', label='SUM-R1-R2')

class gui(qt.QWidget):
    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue
        self.MyUi()

        def on_connect(client, userdata, flags, rc):
            # Subscribes to the user input inside the input_mqtt_topic
            topic_list = self.input_mqtt_topic.currentText()
            print("Connected to topic: "+str(topic_list))
            client.subscribe(topic_list)

        def on_message(client, userdata, msg):
            msg_byte = msg.payload
            msg_array = np.frombuffer(msg_byte, dtype=float, count=-1, offset=0)
            msg_full = np.reshape(msg_array, (40, 2200))
            # when we receive a message (on_message), we run the update_plot function, 
            # which plots the data as soon as it receives a message.
            self.update_plot(np.array(msg_full))
            

        def on_disconnect(client, userdata, rc):
            if rc != 0:
                print("Unexpected disconnection")
            else:
                print("Disconnected")

            self.button_connect.clicked.disconnect()
            self.input_mqtt_topic.setEnabled(True)


        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        self.button_connect.clicked.connect(self.connect)

    def MyUi(self):
        '''
        Method to create the main GUI elements including the matplotlib graph
        and input settings.
        '''
        # The main layout is a QHbox
        hbox = qt.QHBoxLayout()
        #hbox.addStretch(1)
        self.setFixedWidth(1350)
        self.setFixedHeight(750)

        # Make an initially blank matplotlib canvas and axis
        chart_vbox = qt.QVBoxLayout()
        self.fig = Figure(figsize = [9, 3])
        self.static_canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.static_canvas, self)

        # Buttons
        self.widget = qt.QWidget()
        buttons = qt.QVBoxLayout()

        self.input_mqtt_topic = qt.QComboBox()
        self.input_mqtt_topic.addItems(["ac_phys/workxp/live_signals", "ac_phys/workxp/standard", "ac_phys/workxp/test_signals"])
        self.button_connect = qt.QPushButton("Connect")

        buttons.addWidget(self.input_mqtt_topic)
        buttons.addWidget(self.button_connect)

        self.scrollArea = qt.QScrollArea()
        self.scrollArea.setEnabled(True)
        self.scrollArea.setGeometry(QtCore.QRect(20, 10, 431, 401))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 429, 499))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")


        self.checkBox_r0 = qt.QCheckBox("R0", self.scrollAreaWidgetContents)
        self.checkBox_r0.setGeometry(QtCore.QRect(50, 20, 43, 20))
        self.checkBox_r0.setObjectName("checkBox_r0")
        self.checkBox_r1 = QtWidgets.QCheckBox("R1", self.scrollAreaWidgetContents)
        self.checkBox_r1.setGeometry(QtCore.QRect(150, 20, 43, 20))
        self.checkBox_r1.setObjectName("checkBox_r1")
        self.checkBox_r2 = QtWidgets.QCheckBox("R2", self.scrollAreaWidgetContents)
        self.checkBox_r2.setGeometry(QtCore.QRect(250, 20, 43, 20))
        self.checkBox_r2.setObjectName("checkBox_r2")
        self.checkBox_r3 = QtWidgets.QCheckBox("R3", self.scrollAreaWidgetContents)
        self.checkBox_r3.setGeometry(QtCore.QRect(350, 20, 43, 20))
        self.checkBox_r3.setObjectName("checkBox_r3")
        self.checkBox_r4 = QtWidgets.QCheckBox("R4", self.scrollAreaWidgetContents)
        self.checkBox_r4.setGeometry(QtCore.QRect(50, 170, 43, 20))
        self.checkBox_r4.setObjectName("checkBox_r4")
        self.checkBox_r5 = QtWidgets.QCheckBox("R5", self.scrollAreaWidgetContents)
        self.checkBox_r5.setGeometry(QtCore.QRect(150, 170, 43, 20))
        self.checkBox_r5.setObjectName("checkBox_r5")
        self.checkBox_r6 = QtWidgets.QCheckBox("R6", self.scrollAreaWidgetContents)
        self.checkBox_r6.setGeometry(QtCore.QRect(250, 170, 43, 20))
        self.checkBox_r6.setObjectName("checkBox_r6")
        self.checkBox_r7 = QtWidgets.QCheckBox("R7", self.scrollAreaWidgetContents)
        self.checkBox_r7.setGeometry(QtCore.QRect(350, 170, 43, 20))
        self.checkBox_r7.setObjectName("checkBox_r7")
        self.checkBox_r8 = QtWidgets.QCheckBox("R8", self.scrollAreaWidgetContents)
        self.checkBox_r8.setGeometry(QtCore.QRect(50, 340, 43, 20))
        self.checkBox_r8.setObjectName("checkBox_r8")
        self.checkBox_r9 = QtWidgets.QCheckBox("R9", self.scrollAreaWidgetContents)
        self.checkBox_r9.setGeometry(QtCore.QRect(150, 340, 43, 20))
        self.checkBox_r9.setObjectName("checkBox_r9")

        self.checkBox_r5im = QtWidgets.QCheckBox("R5IM", self.scrollAreaWidgetContents)
        self.checkBox_r5im.setGeometry(QtCore.QRect(250, 440, 81, 20))
        self.checkBox_r5im.setObjectName("checkBox_r5im")
        self.checkBox_sum = QtWidgets.QCheckBox("SUM", self.scrollAreaWidgetContents)
        self.checkBox_sum.setGeometry(QtCore.QRect(250, 400, 111, 20))
        self.checkBox_sum.setObjectName("checkBox_sum")
        self.checkBox_sum_r1_r2 = QtWidgets.QCheckBox("SUM - R1  - R2", self.scrollAreaWidgetContents)
        self.checkBox_sum_r1_r2.setGeometry(QtCore.QRect(250, 360, 131, 20))
        self.checkBox_sum_r1_r2.setObjectName("checkBox_sum_r1_r2")
        self.groupBox_r1 = QtWidgets.QGroupBox("R1", self.scrollAreaWidgetContents)
        self.groupBox_r1.setGeometry(QtCore.QRect(120, 40, 91, 111))
        self.groupBox_r1.setObjectName("groupBox_r1")
        self.checkBox_r1blm1 = QtWidgets.QCheckBox("r1blm1", self.groupBox_r1)
        self.checkBox_r1blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r1blm1.setObjectName("checkBox_r1blm1")
        self.checkBox_r1blm2 = QtWidgets.QCheckBox("r1blm2", self.groupBox_r1)
        self.checkBox_r1blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r1blm2.setObjectName("checkBox_r1blm2")
        self.checkBox_r1blm3 = QtWidgets.QCheckBox("r1blm3", self.groupBox_r1)
        self.checkBox_r1blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r1blm3.setObjectName("checkBox_r1blm3")
        self.checkBox_r1blm4 = QtWidgets.QCheckBox("r1blm4", self.groupBox_r1)
        self.checkBox_r1blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r1blm4.setObjectName("checkBox_r1blm4")
        self.groupBox_r2 = QtWidgets.QGroupBox("R2", self.scrollAreaWidgetContents)
        self.groupBox_r2.setGeometry(QtCore.QRect(220, 40, 91, 111))
        self.groupBox_r2.setObjectName("groupBox_r2")
        self.checkBox_r2blm1 = QtWidgets.QCheckBox("r2blm1", self.groupBox_r2)
        self.checkBox_r2blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r2blm1.setObjectName("checkBox_r2blm1")
        self.checkBox_r2blm2 = QtWidgets.QCheckBox("r2blm2", self.groupBox_r2)
        self.checkBox_r2blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r2blm2.setObjectName("checkBox_r2blm2")

        self.checkBox_r2blm3 = QtWidgets.QCheckBox("r2blm3", self.groupBox_r2)
        self.checkBox_r2blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r2blm3.setObjectName("checkBox_r2blm3")
        self.checkBox_r2blm4 = QtWidgets.QCheckBox("r2blm4", self.groupBox_r2)
        self.checkBox_r2blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r2blm4.setObjectName("checkBox_r2blm4")
        self.groupBox_r3 = QtWidgets.QGroupBox("R3", self.scrollAreaWidgetContents)
        self.groupBox_r3.setGeometry(QtCore.QRect(320, 40, 91, 111))
        self.groupBox_r3.setObjectName("groupBox_r3")
        self.checkBox_r3blm4 = QtWidgets.QCheckBox("r3blm4", self.groupBox_r3)
        self.checkBox_r3blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r3blm4.setObjectName("checkBox_r3blm4")
        self.checkBox_r3blm2 = QtWidgets.QCheckBox("r3blm2", self.groupBox_r3)
        self.checkBox_r3blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r3blm2.setObjectName("checkBox_r3blm2")
        self.checkBox_r3blm3 = QtWidgets.QCheckBox("r3blm3", self.groupBox_r3)
        self.checkBox_r3blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r3blm3.setObjectName("checkBox_r3blm3")
        self.checkBox_r3blm1 = QtWidgets.QCheckBox("r3blm1", self.groupBox_r3)
        self.checkBox_r3blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r3blm1.setObjectName("checkBox_r3blm1")

        self.groupBox_r4 = QtWidgets.QGroupBox("R4", self.scrollAreaWidgetContents)
        self.groupBox_r4.setGeometry(QtCore.QRect(20, 210, 91, 111))
        self.groupBox_r4.setObjectName("groupBox_r4")
        self.checkBox_r4blm4 = QtWidgets.QCheckBox("r4blm4", self.groupBox_r4)
        self.checkBox_r4blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r4blm4.setObjectName("checkBox_r4blm4")
        self.checkBox_r4blm1 = QtWidgets.QCheckBox("r4blm1", self.groupBox_r4)
        self.checkBox_r4blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r4blm1.setObjectName("checkBox_r4blm1")
        self.checkBox_r4blm2 = QtWidgets.QCheckBox("r4blm2", self.groupBox_r4)
        self.checkBox_r4blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r4blm2.setObjectName("checkBox_r4blm2")
        self.checkBox_r4blm3 = QtWidgets.QCheckBox("r4blm3", self.groupBox_r4)
        self.checkBox_r4blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r4blm3.setObjectName("checkBox_r4blm3")

        self.groupBox_r5 = QtWidgets.QGroupBox("R5", self.scrollAreaWidgetContents)
        self.groupBox_r5.setGeometry(QtCore.QRect(120, 210, 91, 111))
        self.groupBox_r5.setObjectName("groupBox_r5")
        self.checkBox_r5blm4 = QtWidgets.QCheckBox("r5blm4", self.groupBox_r5)
        self.checkBox_r5blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r5blm4.setObjectName("checkBox_r5blm4")
        self.checkBox_r5blm2 = QtWidgets.QCheckBox("r5blm2", self.groupBox_r5)
        self.checkBox_r5blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r5blm2.setObjectName("checkBox_r5blm2")
        self.checkBox_r5blm1 = QtWidgets.QCheckBox("r5blm1", self.groupBox_r5)
        self.checkBox_r5blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r5blm1.setObjectName("checkBox_r5blm1")
        self.checkBox_r5blm3 = QtWidgets.QCheckBox("r5blm3", self.groupBox_r5)
        self.checkBox_r5blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r5blm3.setObjectName("checkBox_r5blm3")


        self.groupBox_r6 = QtWidgets.QGroupBox("R6", self.scrollAreaWidgetContents)
        self.groupBox_r6.setGeometry(QtCore.QRect(220, 210, 91, 111))
        self.groupBox_r6.setObjectName("groupBox_r6")
        self.checkBox_r6blm4 = QtWidgets.QCheckBox("r6blm4", self.groupBox_r6)
        self.checkBox_r6blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r6blm4.setObjectName("checkBox_r6blm4")
        self.checkBox_r6blm2 = QtWidgets.QCheckBox("r6blm2", self.groupBox_r6)
        self.checkBox_r6blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r6blm2.setObjectName("checkBox_r6blm2")
        self.checkBox_r6blm1 = QtWidgets.QCheckBox("r6blm1", self.groupBox_r6)
        self.checkBox_r6blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r6blm1.setObjectName("checkBox_r6blm1")
        self.checkBox_r6blm3 = QtWidgets.QCheckBox("r6blm3", self.groupBox_r6)
        self.checkBox_r6blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r6blm3.setObjectName("checkBox_r6blm3")

        self.groupBox_r7 = QtWidgets.QGroupBox("R7", self.scrollAreaWidgetContents)
        self.groupBox_r7.setGeometry(QtCore.QRect(320, 210, 91, 111))
        self.groupBox_r7.setObjectName("groupBox_r7")
        self.checkBox_r7blm4 = QtWidgets.QCheckBox("r7blm4", self.groupBox_r7)
        self.checkBox_r7blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r7blm4.setObjectName("checkBox_r7blm4")
        self.checkBox_r7blm1 = QtWidgets.QCheckBox("r7blm1", self.groupBox_r7)
        self.checkBox_r7blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r7blm1.setObjectName("checkBox_r7blm1")
        self.checkBox_r7blm2 = QtWidgets.QCheckBox("r7blm2", self.groupBox_r7)
        self.checkBox_r7blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r7blm2.setObjectName("checkBox_r7blm2")
        self.checkBox_r7blm3 = QtWidgets.QCheckBox("r7blm3", self.groupBox_r7)
        self.checkBox_r7blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r7blm3.setObjectName("checkBox_r7blm3")

        self.groupBox_r8 = QtWidgets.QGroupBox("R8", self.scrollAreaWidgetContents)
        self.groupBox_r8.setGeometry(QtCore.QRect(20, 370, 91, 111))
        self.groupBox_r8.setObjectName("groupBox_r8")
        self.checkBox_r8blm4 = QtWidgets.QCheckBox("r8blm4", self.groupBox_r8)
        self.checkBox_r8blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r8blm4.setObjectName("checkBox_r8blm4")
        self.checkBox_r8blm3 = QtWidgets.QCheckBox("r8blm3", self.groupBox_r8)
        self.checkBox_r8blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r8blm3.setObjectName("checkBox_r8blm3")
        self.checkBox_r8blm2 = QtWidgets.QCheckBox("r8blm2", self.groupBox_r8)
        self.checkBox_r8blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r8blm2.setObjectName("checkBox_r8blm2")
        self.checkBox_r8blm1 = QtWidgets.QCheckBox("r8blm1", self.groupBox_r8)
        self.checkBox_r8blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r8blm1.setObjectName("checkBox_r8blm1")

        self.groupBox_r9 = QtWidgets.QGroupBox("R9", self.scrollAreaWidgetContents)
        self.groupBox_r9.setGeometry(QtCore.QRect(120, 370, 91, 111))
        self.groupBox_r9.setObjectName("groupBox_r9")
        self.checkBox_r9blm4 = QtWidgets.QCheckBox("r9blm4", self.groupBox_r9)
        self.checkBox_r9blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r9blm4.setObjectName("checkBox_r9blm4")
        self.checkBox_r9blm3 = QtWidgets.QCheckBox("r9blm3", self.groupBox_r9)
        self.checkBox_r9blm3.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.checkBox_r9blm3.setObjectName("checkBox_r9blm3")
        self.checkBox_r9blm1 = QtWidgets.QCheckBox("r9blm1", self.groupBox_r9)
        self.checkBox_r9blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r9blm1.setObjectName("checkBox_r9blm1")
        self.checkBox_r9blm2 = QtWidgets.QCheckBox("r9blm2", self.groupBox_r9)
        self.checkBox_r9blm2.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.checkBox_r9blm2.setObjectName("checkBox_r9blm2")

        self.groupBox_r0 = QtWidgets.QGroupBox("R0", self.scrollAreaWidgetContents)
        self.groupBox_r0.setGeometry(QtCore.QRect(20, 40, 91, 111))
        self.groupBox_r0.setObjectName("groupBox_r0")
        self.checkBox_r0blm4 = QtWidgets.QCheckBox("r0blm4", self.groupBox_r0)
        self.checkBox_r0blm4.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.checkBox_r0blm4.setObjectName("checkBox_r0blm4")
        self.checkBox_r0blm1 = QtWidgets.QCheckBox("r0blm1", self.groupBox_r0)
        self.checkBox_r0blm1.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.checkBox_r0blm1.setObjectName("checkBox_r0blm1")
        self.checkBox_r0blm3 = QtWidgets.QCheckBox("r0blm3", self.groupBox_r0)
        self.checkBox_r0blm3.setGeometry(QtCore.QRect(10, 50, 71, 20))
        self.checkBox_r0blm3.setObjectName("checkBox_r0blm3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        

        # Add the widgets to chart layout
        chart_vbox.addWidget(self.static_canvas)
        chart_vbox.addWidget(self.toolbar)

        # Add the layouts to the main layout
        hbox.addLayout(chart_vbox)
        hbox.addLayout(buttons)
        buttons.addWidget(self.scrollArea)

        self.setLayout(hbox)
        self.setGeometry(300, 300, 600, 350)
        self.setWindowTitle("MQTT Plotter")
        self.show()

    def connect(self):
        '''
        Connections to the broker
        '''
        self.client.connect("130.246.57.45", 8883, 60)
        self.client.loop_start()


    def disconnect(self):
        self.client.loop_stop()
        self.client.unsubscribe(self.input_mqtt_topic.text())
        self.client.disconnect()

    
    def update_plot(self, data):
        self.fig.clear()
        self.fig.subplots_adjust(top=0.925, bottom=0.13, left=0.085, right=0.95)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Live Plot of BLM Waveforms updated per second', fontsize=16)
        self.ax.set_xlabel('Time (s)', fontsize = 14)
        self.ax.set_ylabel('Voltage (V)', fontsize = 14)
        self.ax.grid(color = "dimgray")
        self.ax.set_ylim([-0.15, 0.4])
        if self.checkBox_r0blm1.isChecked() == True:
            self.ax.set_ylim([-5.2, 0.4])
        if self.checkBox_r5im.isChecked() == True:
            self.ax.set_ylim([-0.2, 4.0])

        #r0
        if self.checkBox_r0.isChecked() == True:
            self.checkBox_r0blm1.setChecked(True)
            self.checkBox_r0blm3.setChecked(True)
            self.checkBox_r0blm4.setChecked(True)
        #r1
        if self.checkBox_r1.isChecked() == True:
            self.checkBox_r1blm1.setChecked(True)
            self.checkBox_r1blm2.setChecked(True)
            self.checkBox_r1blm3.setChecked(True)
            self.checkBox_r1blm4.setChecked(True)
        #r2
        if self.checkBox_r2.isChecked() == True:
            self.checkBox_r2blm2.setChecked(True)
            self.checkBox_r2blm1.setChecked(True)
            self.checkBox_r2blm3.setChecked(True)
            self.checkBox_r2blm4.setChecked(True)
        #r3
        if self.checkBox_r3.isChecked() == True:
            self.checkBox_r3blm4.setChecked(True)
            self.checkBox_r3blm2.setChecked(True)
            self.checkBox_r3blm3.setChecked(True)
            self.checkBox_r3blm1.setChecked(True)
        #r4
        if self.checkBox_r4.isChecked() == True:
            self.checkBox_r4blm4.setChecked(True)
            self.checkBox_r4blm1.setChecked(True)
            self.checkBox_r4blm2.setChecked(True)
            self.checkBox_r4blm3.setChecked(True)
        #r5
        if self.checkBox_r5.isChecked() == True:
            self.checkBox_r5blm4.setChecked(True)
            self.checkBox_r5blm2.setChecked(True)
            self.checkBox_r5blm1.setChecked(True)
            self.checkBox_r5blm3.setChecked(True)
        #r6
        if self.checkBox_r6.isChecked() == True:
            self.checkBox_r6blm4.setChecked(True)
            self.checkBox_r6blm2.setChecked(True)
            self.checkBox_r6blm1.setChecked(True)
            self.checkBox_r6blm3.setChecked(True)
        #r7
        if self.checkBox_r7.isChecked() == True:
            self.checkBox_r7blm4.setChecked(True)
            self.checkBox_r7blm1.setChecked(True)
            self.checkBox_r7blm2.setChecked(True)
            self.checkBox_r7blm3.setChecked(True)
        #r8
        if self.checkBox_r8.isChecked() == True:
            self.checkBox_r8blm4.setChecked(True)
            self.checkBox_r8blm3.setChecked(True)
            self.checkBox_r8blm2.setChecked(True)
            self.checkBox_r8blm1.setChecked(True)
        #r9
        if self.checkBox_r9.isChecked() == True:
            self.checkBox_r9blm4.setChecked(True)
            self.checkBox_r9blm3.setChecked(True)
            self.checkBox_r9blm1.setChecked(True)
            self.checkBox_r9blm2.setChecked(True)
        if self.checkBox_r0blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[0])), c = 'blue', ls='-')
        if self.checkBox_r0blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[1])), c = 'blue', ls='-.')
        if self.checkBox_r0blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[2])), c = 'blue', ls=':')
        if self.checkBox_r1blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[3])), c = 'darkviolet', ls='-')
        if self.checkBox_r1blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[4])), c = 'darkviolet', ls='--')
        if self.checkBox_r1blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[5])), c = 'darkviolet', ls='-.')
        if self.checkBox_r1blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[6])), c = 'darkviolet', ls=':')
        if self.checkBox_r2blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[7])), c = 'deeppink', ls='-')
        if self.checkBox_r2blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[8])), c = 'deeppink', ls='--')
        if self.checkBox_r2blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[9])), c = 'deeppink', ls='-.')
        if self.checkBox_r2blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[10])), c = 'deeppink', ls=':')
        if self.checkBox_r3blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[11])), c = 'crimson', ls='-')
        if self.checkBox_r3blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[12])), c = 'crimson', ls='--')
        if self.checkBox_r3blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[13])), c = 'crimson', ls='-.')
        if self.checkBox_r3blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[14])), c = 'crimson', ls=':')
        if self.checkBox_r4blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[15])), c = 'coral', ls='-')
        if self.checkBox_r4blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[16])), c = 'coral', ls='--')
        if self.checkBox_r4blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[17])), c = 'coral', ls='-.')
        if self.checkBox_r4blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[18])), c = 'coral', ls=':')
        if self.checkBox_r5blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[19])), c = 'gold', ls='-')
        if self.checkBox_r5blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[20])), c = 'gold', ls='--')
        if self.checkBox_r5blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[21])), c = 'gold', ls='-.')
        if self.checkBox_r5blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[22])), c = 'gold', ls=':')
        if self.checkBox_r6blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[23])), c = 'lime', ls='-')
        if self.checkBox_r6blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[24])), c = 'lime', ls='--')
        if self.checkBox_r6blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[25])), c = 'lime', ls='-.')
        if self.checkBox_r6blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[26])), c = 'lime', ls=':')
        if self.checkBox_r7blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[27])), c = 'forestgreen', ls='-')
        if self.checkBox_r7blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[28])), c = 'forestgreen', ls='--')
        if self.checkBox_r7blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[29])), c = 'forestgreen', ls='-.')
        if self.checkBox_r7blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[30])), c = 'forestgreen', ls=':')
        if self.checkBox_r8blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[31])), c = 'turquoise', ls='-')
        if self.checkBox_r8blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[32])), c = 'turquoise', ls='--')
        if self.checkBox_r8blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[33])), c = 'turquoise', ls='-.')
        if self.checkBox_r8blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[34])), c = 'turquoise', ls=':')
        if self.checkBox_r9blm1.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[35])), c = 'cornflowerblue', ls='-')
        if self.checkBox_r9blm2.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[36])), c = 'cornflowerblue', ls='--')
        if self.checkBox_r9blm3.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[37])), c = 'cornflowerblue', ls='-.')
        if self.checkBox_r9blm4.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[38])), c = 'cornflowerblue', ls=':')
        if self.checkBox_r5im.isChecked() == True:
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), ((data[39])), c = 'navy')
        if self.checkBox_sum.isChecked() == True:
            tot_sum = np.sum((data), axis = 0)
            blm_sum = tot_sum - (data[0]) - (data[39])
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), blm_sum, c = 'black')
        if self.checkBox_sum_r1_r2.isChecked() == True:
            tot_sum = (np.sum((data), axis = 0))
            blm_sum2 = tot_sum - ((data[39])) - (data[0]) - (data[1]) - (data[2]) - (data[3]) - (data[4]) - (data[5]) - (data[6])
            self.ax.plot(np.linspace(-0.5, 10.5, num=2200, endpoint=True), blm_sum2, c = 'gray')

        self.ax.legend(handles=[r0_patch, r1_patch, r2_patch, r3_patch, r4_patch, r5_patch, r6_patch, r7_patch, r8_patch, r9_patch, im_patch, sum_patch, sum2_patch], loc='best', fontsize = "x-small")
        
        self.static_canvas.draw()

if __name__ == '__main__':
    data_queue = multiprocessing.Queue()

    app = qt.QApplication(sys.argv)
    window = gui(data_queue)
    window.show()
    app.exec()