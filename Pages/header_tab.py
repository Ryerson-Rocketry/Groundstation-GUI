import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore 
import PySide6.QtWidgets

class HeaderTabUI(QtCore.QObject):
    send_signal = PySide6.QtCore.Signal(int) #emit with a int signature

    def __init__(self):
        super().__init__()
        self.graph_button = Button("Graph")
        self.full_view_button = Button("Full View")
        self.map_button = Button("Map")  

        self.tab_layout_container = QtWidgets.QWidget()
        self.tab_layout = QtWidgets.QHBoxLayout(self.tab_layout_container)

        self.tab_layout.addWidget(self.full_view_button)
        self.tab_layout.addWidget(self.graph_button) 
        #self.tab_layout.addWidget(self.map_button)

        self.full_view_button.clicked.connect (lambda x: self.send_page_layout_index(0))
        self.graph_button.clicked.connect (lambda x: self.send_page_layout_index(1))
        self.map_button.clicked.connect (lambda x: self.send_page_layout_index(2))

    @QtCore.Slot() 
    def send_page_layout_index(self, index):
        self.send_signal.emit(index)

class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)

        
