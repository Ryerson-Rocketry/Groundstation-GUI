import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets

import time
import numpy

#Map dependency
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy #unused

#Graph dependency
from matplotlib.figure import Figure

#For handling backend use of matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Graph

#Custom Classes/Functions
import DataRead

class mainWindowUI(object):
    def setup(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        self.label1 = QtWidgets.QLabel()
        self.label1.setText("Acceleration: 0")
        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Pressure: 0")
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("Placeholder: 0")
        self.label4 = QtWidgets.QLabel()
        self.label4.setText("Current Time: ")

        self.buttonLeft = QtWidgets.QPushButton()
        self.buttonLeft.setText("Start")

        self.buttonZoomIn = Button("+")
        self.buttonZoomOut = Button("-")

        self.buttonPanLeft = Button("<")
        self.buttonPanRight = Button(">") 
        self.buttonPanDown = Button("v")
        self.buttonPanUp = Button("^")

        self.buttonMapFocus = Button("Unfocus on rocket")

        self.tabButton1 = Button("Pressure:")
        self.tabButton2 = Button("Temperature:")
        self.tabButton3 = Button("Signal Strength:")
        self.tabButton4 = Button("Battery Voltage:")

        self.threadUseButton = Button("Time")

        # Add the plotTrajectoryButton
        self.plotTrajectoryButton = QtWidgets.QPushButton()
        self.plotTrajectoryButton.setText("Plot Trajectory")
        
        # Layouts ---
        tabLayout = QtWidgets.QHBoxLayout()
        tabLayout.addWidget(self.tabButton1)
        tabLayout.addWidget(self.tabButton2)
        tabLayout.addWidget(self.tabButton3)
        tabLayout.addWidget(self.tabButton4)

        self.dataLayout = QtWidgets.QGridLayout() 
        self.StackedGraphs = QtWidgets.QStackedLayout()

        for i in range(len(MainWindow.dataPlots)):
            self.StackedGraphs.addWidget(MainWindow.dataPlots[i])

        self.dataLayout.addLayout(self.StackedGraphs, 2, 0, 1 , 4) 
        
        dataChildLayout = QtWidgets.QVBoxLayout()
        
        dataChildLayout.addWidget(self.label1) 
        dataChildLayout.addWidget(self.label2)
        dataChildLayout.addWidget(self.label3)
        dataChildLayout.addWidget(self.label4)

        self.dataLayout.addLayout(tabLayout,1,0)
        self.dataLayout.addLayout(dataChildLayout,3,0)
        self.dataLayout.addWidget(self.buttonLeft, 4 ,0)
        self.dataLayout.addWidget(self.threadUseButton, 4, 1)
        self.dataLayout.addWidget(self.buttonMapFocus, 4, 2)
        self.dataLayout.addWidget(self.plotTrajectoryButton, 4, 3)  # Add the plotTrajectoryButton

        self.layoutMain = QtWidgets.QGridLayout()
        self.layoutMain.addWidget(MainWindow.Map, 0,0,8,3) 
        self.layoutMain.addWidget(self.buttonZoomIn, 9,0,1,1)
        self.layoutMain.addWidget(self.buttonZoomOut, 9,2,1,1)
        self.layoutMain.addWidget(self.buttonPanLeft, 10,0,1,1)
        self.layoutMain.addWidget(self.buttonPanRight, 10,2,1,1)
        self.layoutMain.addWidget(self.buttonPanUp, 9,1,1,1)
        self.layoutMain.addWidget(self.buttonPanDown, 10,1,1,1)
        self.layoutMain.addLayout(self.dataLayout, 1, 3, 1, 2)

class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)

