import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore 
import PySide6.QtWidgets

class GraphDisplayUI(QtCore.QObject):
    send_signal = PySide6.QtCore.Signal(int) #emit with a int signature

    def __init__(self, MainGUI):
        super().__init__()

        self.graph_layout_container = QtWidgets.QWidget()
        self.graph_layout = QtWidgets.QVBoxLayout(self.graph_layout_container)

        self.graph_layout.addWidget(QtWidgets.QLabel("#"))


