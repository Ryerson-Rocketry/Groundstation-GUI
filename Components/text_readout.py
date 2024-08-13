import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets



class TextReadoutUI(QtCore.QObject):
    def __init__(self, mainWindow):
        super().__init__()
        self.label1 = QtWidgets.QLabel()
        self.label1.setText("Accelerometer X-Axis: 0")
        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Accelerometer Y-Axis: 0")
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("Accelerometer Z-Axis: 0")

        self.text_readout_layout_container = QtWidgets.QWidget()
        self.text_readout_layout = QtWidgets.QVBoxLayout(self.text_readout_layout_container)
        
        self.text_readout_layout.addWidget(self.label1) 
        self.text_readout_layout.addWidget(self.label2)
        self.text_readout_layout.addWidget(self.label3)

    def set_readout_text(self, accel_x, accel_y, accel_z):
        self.label1.setText("Accelerometer X-Axis: " + accel_x)
        self.label2.setText("Accelerometer Y-Axis: " + accel_y)
        self.label3.setText("Accelerometer Z-Axis: " + accel_z)


