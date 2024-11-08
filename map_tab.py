from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtWidgets

class MapTabUI(QtCore.QObject):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.map_tab_header = QtWidgets.QHBoxLayout()
        self.tabButton1 = Button("GS:")
        self.tabButton2 = Button("Featherweight:")

        self.PLACEHOLDER = QtWidgets.QLabel("placeholder")
        
        self.map_tab_header.addWidget(self.tabButton1)
        self.map_tab_header.addWidget(self.tabButton2)

        self.stacked_maps = QtWidgets.QStackedLayout()
        self.stacked_maps.addWidget(mainWindow.mainGUI.Map)
        self.stacked_maps.addWidget(self.PLACEHOLDER)

        self.map_page_layout_container = QtWidgets.QWidget()
        self.map_page_layout = QtWidgets.QVBoxLayout(self.map_page_layout_container)

        self.map_page_layout.addLayout(self.map_tab_header)
        self.map_page_layout.addLayout(self.stacked_maps)

        self.tabButton1.clicked.connect(lambda x: self.tabSwitching(0))
        self.tabButton2.clicked.connect(lambda x: self.tabSwitching(1))


    @QtCore.Slot() #Tab switching
    def tabSwitching(self, tabNum):
        self.stacked_maps.setCurrentIndex(tabNum)

        

class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)