import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets

import time
import numpy


#Custom Classes/Functions
import DataRead
import MainWindow

from Data_Classes import graphing



LAUNCH_POINT_X = 0
LAUNCH_POINT_Y = 0

class MainWidget(QtWidgets.QMainWindow): #Main Class
    def __init__(self):
        super(MainWidget, self).__init__()
        
        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("Rocketry Ground Station GUI")
        self.resize(1800,800)

        #Graph & Map & Other Widget Class Init ---
        self.DataSet = DataRead.DataTrack()

        self.dataPlots = []
        self.secondary_data_plots = []
        for i in range(4):
            self.dataPlots.append(graphing.Matplot())
            self.dataPlots[i].InitGraph("Time (Sec)", self.DataSet.graphDict[i + 3] + " (" + self.DataSet.graph_dict_units[i + 3] + ")" , self.DataSet.graphDict[i + 3] + "-Time Graph", i)
            self.dataPlots[i].graphIndex = i+3

            self.secondary_data_plots.append(graphing.Matplot())
            self.secondary_data_plots[i].InitGraph("Time (Sec)", self.DataSet.graphDict[i + 3] + " (" + self.DataSet.graph_dict_units[i + 3] + ")" , self.DataSet.graphDict[i + 3] + "-Time Graph", i)
            self.secondary_data_plots[i].graphIndex = i+3
        
        self.Map = graphing.Map(self.DataSet)   
        self.mapState = False
        self.graphState = False

        #Graph & Map Class Init ---

        self.mainWindowUI = MainWindow.mainWindowUI(self)
    
        widget = QtWidgets.QWidget(self)
        widget.setLayout(self.mainWindowUI.main_layout)
        self.setCentralWidget(widget)

        #Signals
        self.mainWindowUI.buttonLeft.clicked.connect(self.buttonLeftInteraction) 

        self.mainWindowUI.tabButton1.clicked.connect(lambda x: self.tabSwitching(0))
        self.mainWindowUI.tabButton2.clicked.connect(lambda x: self.tabSwitching(1))
        self.mainWindowUI.tabButton3.clicked.connect(lambda x: self.tabSwitching(2))
        self.mainWindowUI.tabButton4.clicked.connect(lambda x: self.tabSwitching(3))
        
        self.mainWindowUI.buttonZoomIn.clicked.connect(lambda x: self.mapZoom(1))
        self.mainWindowUI.buttonZoomOut.clicked.connect(lambda x: self.mapZoom(2))

        """
        self.mainWindowUI.buttonPanLeft.clicked.connect(lambda x: self.mapPan(1))
        self.mainWindowUI.buttonPanRight.clicked.connect(lambda x: self.mapPan(2))
        self.mainWindowUI.buttonPanUp.clicked.connect(lambda x: self.mapPan(3))
        self.mainWindowUI.buttonPanDown.clicked.connect(lambda x: self.mapPan(4))
        """

    def keyPressEvent(self, event):
        match(event.text()):
            case "w":
                self.mapPan(1)
            case "a":
                self.mapPan(2)
            case "d":
                self.mapPan(3)
            case "s":
                self.mapPan(4)              
            case _:
                print (event.text())
                return

    #Slots         
    @QtCore.Slot()    
    def mapZoom(self, zoomlevel):
        self.Map.mapZoom(zoomlevel, self.DataSet)
        self.Map.draw()

    @QtCore.Slot()    
    def mapPan(self, panType):
        self.Map.mapPan(panType, self.DataSet)
        self.Map.draw()

    @QtCore.Slot() #Tab switching
    def tabSwitching(self, tabNum):
        self.mainWindowUI.StackedGraphs.setCurrentIndex(tabNum)
        
        if (tabNum == 3):
            self.mainWindowUI.text_readout_module.text_readout_layout_container.setVisible(True);
        else:
            self.mainWindowUI.text_readout_module.text_readout_layout_container.setVisible(False);
    
    @QtCore.Slot()
    def buttonLeftInteraction(self):    
        self.mainWindowUI.buttonLeft.setText("Stop")

        def execute(): #map thread
            
            while True:
                while self.graphState == True:

                    self.DataSet.maprunning = True

                    i = self.DataSet.latestElement

                    self.Map.mapPlotting()
                    self.Map.draw()
                    
                    #print (str(self.DataSet.InternalData[0][i]) + "," + str(self.DataSet.InternalData[1][i])) #debug
                    self.mainWindowUI.text_readout_module.set_readout_text(str(self.DataSet.InternalData[6][i]), str(self.DataSet.InternalData[7][i]), str(self.DataSet.InternalData[8][i]))

                    self.DataSet.maprunning = False

                    self.graphState = False
                    self.mapState = True #tells the graph thread that it can plot

                time.sleep(0.1)
               
        def execute2(): #graph thread (not needed?)
            while True:
                while self.mapState == True: 

                    for i in range(len(self.dataPlots)): #Plots all graphs at once

                        self.dataPlots[i].plotPoint(self.DataSet, i)
                        self.secondary_data_plots[i].plotPoint(self.DataSet, i)


                    self.mapState = False

                time.sleep(0.1)

        def execute3(): #new data element check
            while True:
                
                DataRead.FileReadSequential(self.DataSet)

                if (DataRead.FileReadSequential(self.DataSet) != False):

                    self.graphState = True

                time.sleep(0.1)

        thread = WorkerThread(execute)
        thread2 = WorkerThread(execute2) 
        thread3 = WorkerThread(execute3) 
        self.threadpool.start(thread)
        self.threadpool.start(thread2)
        self.threadpool.start(thread3)


        
#Multithreading
class WorkerThread(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(WorkerThread, self).__init__()
        
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
    
    @QtCore.Slot()  
    def run(self):
        self.fn(*self.args, **self.kwargs)



        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    MainWindow = MainWidget()

    MainWindow.show()

    sys.exit(app.exec())

