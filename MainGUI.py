import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets

import time

import DataRead

class MyWidget(QtWidgets.QWidget): #Class for general UI stuff (buttons and text)
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Dot Mover")
        self.resize(800,800)

        self.label = QtWidgets.QLabel()
        self.label.setText("Enter Coordinates of where you want the dot to move")

        self.TextBoxX = QtWidgets.QTextEdit()
        self.TextBoxX.setFixedWidth(400)
        self.TextBoxX.setFixedHeight(200)
        
        self.TextBoxY = QtWidgets.QTextEdit()
        self.TextBoxY.setFixedWidth(400)
        self.TextBoxY.setFixedHeight(200)

        self.buttonLeft = QtWidgets.QPushButton()
        self.buttonLeft.setText("Enter Coordinates")

        self.buttonRight = QtWidgets.QPushButton()
        self.buttonRight.setText("Preset Coordinate List")

        #Graphical -------
        
        #Painter Instance
        #self.map = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("GTAAREA.jpg")) #A graphical object that takes in a pixelmap object

        self.dot = QtWidgets.QGraphicsRectItem() #A graphical object
        self.dot.setRect(10,10,10,10)

        self.scene = QtWidgets.QGraphicsScene() #Scene object that contains graphical object
        #self.scene.addItem(self.map)
        self.scene.addItem(self.dot)

        self.view = QtWidgets.QGraphicsView(self.scene) #A object (window) to show the scene
        self.view.setFixedWidth(800)
        self.view.setFixedHeight(500)

        #creates an object for a grid type window layout, above objects can be added to the layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.view, 0,0,1,2) #to be contained in cell row:0,column:0, spanning 1 row and 2 columns
        layout.addWidget(self.label)
        layout.addWidget(self.TextBoxX, 3 ,0)
        layout.addWidget(self.TextBoxY,3 , 1)
        layout.addWidget(self.buttonLeft,4, 0)
        layout.addWidget(self.buttonRight, 4 ,1)

        self.buttonLeft.clicked.connect(self.buttonLeftInteraction) #when interacted with, executes function within the parameter
        self.buttonRight.clicked.connect(self.buttonRightInteraction) #when interacted with, executes function within the parameter
        
    @QtCore.Slot()
    def buttonLeftInteraction(self):
        #using setpos method and the float casted contents of the textboxes, the dot location can then be changed
        self.dot.setPos(float(self.TextBoxX.toPlainText()),float(self.TextBoxY.toPlainText()))
        
    @QtCore.Slot()
    def buttonRightInteraction(self):
        CoordinateArray = DataRead.fileRead() #A 2D array for x,y coordinates
        
        for i in range(len(CoordinateArray[0])):

            QtCore.QCoreApplication.processEvents() #apparently a "bad" way to update the gui as the for loop progresses. Need to figure out how to use the built in Qthread/multithreading to do it properly
            
            self.dot.setPos(float(CoordinateArray[0][i]),float(CoordinateArray[1][i])) #sets x and y from CoordinateArray
            print (CoordinateArray[0][i] + "," + CoordinateArray[1][i]) #debug
            time.sleep(1)


#class ActionThread ()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()


    
    widget.show()

    sys.exit(app.exec())



