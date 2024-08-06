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

from Components import text_readout

GRAPH_SIZE_WIDTH = 1000
GRAPH_SIZE_HEIGHT = 100

class mainWindowUI(object):

    def setup(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        #UI module setup
        self.text_readout_module = text_readout.TextReadoutUI()
        self.text_readout_module.setup(self)

        self.buttonLeft = QtWidgets.QPushButton()
        self.buttonLeft.setText("Start")

        self.buttonZoomIn = Button("+")
        self.buttonZoomOut = Button("-")

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
        
        #Layouts ---
        tabLayout = QtWidgets.QHBoxLayout()
        tabLayout.addWidget(self.tabButton1)
        tabLayout.addWidget(self.tabButton2)
        tabLayout.addWidget(self.tabButton3)
        tabLayout.addWidget(self.tabButton4)

        #creates an object for a grid type window layout, above objects can be added to the layout
        self.dataLayout = QtWidgets.QGridLayout() 
        self.StackedGraphs = QtWidgets.QStackedLayout()

        for i in range(len(MainWindow.dataPlots)):
            self.StackedGraphs.addWidget(MainWindow.dataPlots[i])
            MainWindow.dataPlots[i].resize(PySide6.QtCore.QSize(GRAPH_SIZE_WIDTH,GRAPH_SIZE_HEIGHT))

        self.dataLayout.addLayout(self.StackedGraphs, 2, 0, 1 , 4) 

        self.dataLayout.addLayout(tabLayout,1,0)
        self.dataLayout.addLayout(self.text_readout_module.text_readout_layout,3,0)
        self.dataLayout.addWidget(self.buttonLeft, 4 ,0)
        self.dataLayout.addWidget(self.threadUseButton, 4, 1)
        self.dataLayout.addWidget(self.buttonMapFocus, 4, 2)

        self.layoutMain = QtWidgets.QGridLayout()
        self.layoutMain.addWidget(MainWindow.Map, 0,0,8,3) #to be contained in cell row:0,column:0, spanning 8 row and 3 columns
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

