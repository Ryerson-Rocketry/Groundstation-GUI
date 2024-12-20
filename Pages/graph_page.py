import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore 
import PySide6.QtWidgets


class GraphPageUI(QtCore.QObject):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.graph_tab_header = QtWidgets.QHBoxLayout()
        self.tabButton1 = Button("Pressure:")
        self.tabButton2 = Button("Temperature:")
        self.tabButton3 = Button("Battery Voltage:")
        self.tabButton4 = Button("Acceleration:")
        
        self.graph_tab_header.addWidget(self.tabButton1)
        self.graph_tab_header.addWidget(self.tabButton2)
        self.graph_tab_header.addWidget(self.tabButton3)
        self.graph_tab_header.addWidget(self.tabButton4)

        self.secondary_stacked_graphs = QtWidgets.QStackedLayout()

        for i in range(len(mainWindow.mainGUI.dataPlots)):
            self.secondary_stacked_graphs.addWidget(mainWindow.mainGUI.secondary_data_plots[i])

        self.graph_page_layout_container = QtWidgets.QWidget()
        self.graph_page_layout = QtWidgets.QVBoxLayout(self.graph_page_layout_container)

        self.graph_page_layout.addLayout(self.graph_tab_header)
        self.graph_page_layout.addLayout(self.secondary_stacked_graphs)

        self.tabButton1.clicked.connect(lambda x: self.tabSwitching(0))
        self.tabButton2.clicked.connect(lambda x: self.tabSwitching(1))
        self.tabButton3.clicked.connect(lambda x: self.tabSwitching(2))
        self.tabButton4.clicked.connect(lambda x: self.tabSwitching(3))

    @QtCore.Slot() #Tab switching
    def tabSwitching(self, tabNum):
        self.mainWindow.mainGUI.currentGraphTab = tabNum + 3
        self.secondary_stacked_graphs.setCurrentIndex(tabNum)

        if (tabNum == 3):
            self.mainWindow.text_readout_module.text_readout_layout_container.setVisible(True);
        else:
            self.mainWindow.text_readout_module.text_readout_layout_container.setVisible(False);
        

        
class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)