import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets

import time
import numpy


#Custom Classes/Functions
import DataRead

from Components import text_readout
from Components import graph_display

from Pages import header_tab as tabpage
from Pages import graph_page as graphpage



GRAPH_SIZE_WIDTH = 1000
GRAPH_SIZE_HEIGHT = 100

class mainWindowUI(QtCore.QObject):
    def __init__(self, mainGUI):
        super().__init__()
        self.mainGUI = mainGUI

        #UI module setup
        self.text_readout_module = text_readout.TextReadoutUI(self)

        self.graph_display_module = graph_display.GraphDisplayUI(self)

        self.header_tab_module = tabpage.HeaderTabUI()
        self.graph_page_module = graphpage.GraphPageUI(self)
        #UI module setup

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
        self.tabButton3 = Button("Battery Voltage:")
        self.tabButton4 = Button("Acceleration:")
        
        #Layouts ---
        tabLayout = QtWidgets.QHBoxLayout()
        tabLayout.addWidget(self.tabButton1)
        tabLayout.addWidget(self.tabButton2)
        tabLayout.addWidget(self.tabButton3)
        tabLayout.addWidget(self.tabButton4)

        #creates an object for a grid type window layout, above objects can be added to the layout
        self.dataLayout = QtWidgets.QGridLayout() 

        self.overall_layout_container = QtWidgets.QWidget()
        self.overall_layout = QtWidgets.QGridLayout(self.overall_layout_container)

        self.StackedGraphs = QtWidgets.QStackedLayout()

        for i in range(len(mainGUI.dataPlots)):
            self.StackedGraphs.addWidget(mainGUI.dataPlots[i])
            mainGUI.dataPlots[i].resize(PySide6.QtCore.QSize(GRAPH_SIZE_WIDTH,GRAPH_SIZE_HEIGHT))

        self.dataLayout.addLayout(self.StackedGraphs, 2, 0, 1 , 4) 
        self.dataLayout.addLayout(tabLayout,1,0)
        self.dataLayout.addWidget(self.text_readout_module.text_readout_layout_container , 3, 0)
        self.text_readout_module.text_readout_layout_container.setVisible(False)

        self.dataLayout.addWidget(self.buttonLeft, 4 ,0)
        #self.dataLayout.addWidget(self.buttonMapFocus, 4, 1)

        self.overall_layout.addWidget(mainGUI.Map, 1,0,8,3) #to be contained in cell row:0,column:0, spanning 8 row and 3 columns
        """
        self.overall_layout.addWidget(self.buttonZoomIn, 9,0,1,1)
        self.overall_layout.addWidget(self.buttonZoomOut, 9,2,1,1)
        self.overall_layout.addWidget(self.buttonPanLeft, 10,0,1,1)
        self.overall_layout.addWidget(self.buttonPanRight, 10,2,1,1)
        self.overall_layout.addWidget(self.buttonPanUp, 9,1,1,1)
        self.overall_layout.addWidget(self.buttonPanDown, 10,1,1,1)
        """
        self.overall_layout.addLayout(self.dataLayout, 1, 3, 1, 2)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.stacked_page_layout = QtWidgets.QStackedLayout()
        self.stacked_page_layout.addWidget(self.overall_layout_container)
        self.stacked_page_layout.addWidget(self.graph_page_module.graph_page_layout_container)

        self.main_layout.addWidget(self.header_tab_module.tab_layout_container)
        self.main_layout.addLayout(self.stacked_page_layout)

        self.header_tab_module.send_signal.connect(self.change_pages)

    @QtCore.Slot()
    def change_pages(self, value):
        self.stacked_page_layout.setCurrentIndex(value)


class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)

