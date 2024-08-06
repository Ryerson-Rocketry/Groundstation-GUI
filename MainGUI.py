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
import MainWindow

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
        for i in range(4):
            self.dataPlots.append(Matplot())
            self.dataPlots[i].InitGraph("Time (Sec)", self.DataSet.graphDict[i + 3] + " (" + self.DataSet.graph_dict_units[i + 3] + ")" , self.DataSet.graphDict[i + 3] + "-Time Graph")
            self.dataPlots[i].graphIndex = i+3
        
        self.Map = Map(self.DataSet)   
        self.mapState = False
        self.graphState = False

        #Graph & Map Class Init ---

        self.mainWindowUI = MainWindow.mainWindowUI()
        self.mainWindowUI.setup(self)
    
        widget = QtWidgets.QWidget(self)
        widget.setLayout(self.mainWindowUI.layoutMain)
        self.setCentralWidget(widget)

        #Signals
        self.mainWindowUI.buttonLeft.clicked.connect(self.buttonLeftInteraction) 
        self.mainWindowUI.threadUseButton.clicked.connect(self.threadUseCheck) 

        #Note that there will be mismatch with indexes of other lists
        self.mainWindowUI.tabButton1.clicked.connect(lambda x: self.tabSwitching(3))
        self.mainWindowUI.tabButton2.clicked.connect(lambda x: self.tabSwitching(4))
        self.mainWindowUI.tabButton3.clicked.connect(lambda x: self.tabSwitching(5))
        self.mainWindowUI.tabButton4.clicked.connect(lambda x: self.tabSwitching(6))

        self.mainWindowUI.buttonZoomIn.clicked.connect(lambda x: self.mapZoom(1))
        self.mainWindowUI.buttonZoomOut.clicked.connect(lambda x: self.mapZoom(2))

        self.mainWindowUI.buttonPanLeft.clicked.connect(lambda x: self.mapPan(1))
        self.mainWindowUI.buttonPanRight.clicked.connect(lambda x: self.mapPan(2))
        self.mainWindowUI.buttonPanUp.clicked.connect(lambda x: self.mapPan(3))
        self.mainWindowUI.buttonPanDown.clicked.connect(lambda x: self.mapPan(4))

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
        self.DataSet.currentGraphTab = tabNum
        print (tabNum) #debug 
        self.mainWindowUI.StackedGraphs.setCurrentIndex(tabNum - 3)

    @QtCore.Slot()
    def threadUseCheck(self):
        def execute():
            self.DataSet.timeSync()
            self.mainWindowUI.label4.setText("Current Time: " + str(self.DataSet.currentTime))

        thread = WorkerThread(execute)
        self.threadpool.start(thread)
    
    @QtCore.Slot()
    def buttonLeftInteraction(self):    

        def execute(): #map thread
            
            while True:
                while self.graphState == True:

                    self.DataSet.maprunning = True

                    i = self.DataSet.latestElement

                    self.Map.mapPlotting()
                    self.Map.draw()
                    
                    #print (str(self.DataSet.InternalData[0][i]) + "," + str(self.DataSet.InternalData[1][i])) #debug
                    self.mainWindowUI.text_readout_module.set_readout_text(str(self.DataSet.InternalData[7][i]), str(self.DataSet.InternalData[8][i]), str(self.DataSet.InternalData[9][i]))

                    self.DataSet.maprunning = False

                    self.graphState = False
                    self.mapState = True #tells the graph thread that it can plot

                time.sleep(0.1)
               
        def execute2(): #graph thread (not needed?)
            while True:
                while self.mapState == True: 

                    for i in range(len(self.dataPlots)): #Plots all graphs at once
                        self.dataPlots[i].plotPoint(self.DataSet, i)

                    self.mapState = False

                time.sleep(0.1)

        def execute3(): #newdataelementcheck
            while True:
                
                DataRead.FileReadSequential(self.DataSet)
                #print ("test")
                if (DataRead.FileReadSequential(self.DataSet) != False):

                    self.graphState = True
                        #self.mapState = True

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

class Matplot(Graph):

    #Inits top level figure and the actual graph
    def __init__(self):
        super(Matplot, self).__init__(Figure())
        self.figure = Figure()
        self.canvas = Graph (self.figure)
        self.axes = self.figure.add_subplot(111) 

        self.graphIndex = 0

        self.x_string = ""
        self.y_string = ""
        self.title_string = ""

    #Defines graph axes
    def InitGraph (self, xlabel, ylabel, title):
        self.x_string = xlabel
        self.y_string = ylabel
        self.title_string = title

        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)

    def plotPoint (self, DataSet, graphIndex):
        if (DataSet.tolerance(graphIndex) == False):
            self.axes.clear()
            
            #axis labels and titles need to be readded after graphs are cleared
            self.axes.set_xlabel(self.x_string)
            self.axes.set_ylabel(self.y_string)
            self.axes.set_title(self.title_string)

            self.axes.plot((DataSet.InternalData[2]), (DataSet.InternalData[DataSet.currentGraphTab]), marker='o', linewidth = 0.1, markersize = 2 )
            self.draw()
        

class Map(Graph):
    def __init__(self, DataSet):
        super(Map, self).__init__()
        self.zoomScale = 1.0 #initial zoom
        self.panLocation = [0.0,0.0]
        self.pan_lat = 0.0
        self.pan_long = 0.0

        self.DataSet = DataSet
        self.figure = plt.figure()
        self.canvas = Graph (self.figure)
        self.axe = self.figure.add_subplot(1,1,1, projection = ccrs.PlateCarree())

        #self.fig, self.ax = plt.subplots(1,1,1, projection = ccrs.PlateCarree())

        self.initMap() 


    def initMap(self): #Since main method of rendering the map is to draw , clear, and redraw the map, defined a function to do that
        self.axes = plt.axes(projection=ccrs.PlateCarree())
        self.axes.coastlines()
        
        self.axes.gridlines(draw_labels=True,dms = True,x_inline = False, y_inline = False) #grid and coordinate axises

        #self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'cultural', name= 'urban_areas', scale='10m', facecolor='grey'))
        #self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'raster', name= 'natural_earth1', scale='50m'))

        #preset features 
        self.axes.add_feature(cfeature.LAKES)
        self.axes.add_feature(cfeature.RIVERS)
        self.axes.add_feature(cfeature.OCEAN)
        self.axes.add_feature(cfeature.LAND)
        self.axes.add_feature(cfeature.BORDERS)

    def mapPlotting(self):
        self.figure.clear()

        try:
            base_lat, base_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement]), float(self.DataSet.InternalData[1][self.DataSet.latestElement])  #-79.38 , 43.65
            self.pan_lat, self.pan_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement]) + self.panLocation[0], float(self.DataSet.InternalData[1][self.DataSet.latestElement]) + self.panLocation[1] #updates the pan location relative to rocket
        except:
            return
        
        self.initMap()
        self.mapZoom()

        self.axes.set_extent([base_lat - self.zoomScale ,base_lat + self.zoomScale ,base_long - self.zoomScale, base_long + self.zoomScale]) # Zoom Scale

        self.axes.plot (base_lat , base_long, color = 'blue', linewidth = '2', marker= 'o' ) #Rocket
        self.axes.plot ((self.pan_lat) ,(self.pan_long), color = 'red', linewidth = '3', marker= 'x')  #Map Focus Point
        self.axes.plot (LAUNCH_POINT_X , LAUNCH_POINT_Y, color = 'red', linewidth = '2', marker= 'o') #Launch Point
        self.axes.text (LAUNCH_POINT_X , LAUNCH_POINT_Y ,"Launch Point")

    def mapZoom(self):
        self.zoomScale = max((self.DataSet.InternalData[0][self.DataSet.latestElement]) - LAUNCH_POINT_X + 1, (LAUNCH_POINT_Y - (self.DataSet.InternalData[0][self.DataSet.latestElement])) + 1)
        self.zoomScale = abs(self.zoomScale)
        
        #print (self.zoomScale)


    def mapPan(self, panType, dataSet):

        if (dataSet.maprunning == True):
            return 
        
        self.figure.clear()
    
        match(panType):
            case 1: #X Left
                self.panLocation[0] = self.panLocation[0] - 0.5
            case 2: #X right
                self.panLocation[0] = self.panLocation[0] + 0.5
            case 3: #Y up
                self.panLocation[1] = self.panLocation[1] + 0.5
            case 4: #Y down
                self.panLocation[1] = self.panLocation[1] - 0.5

        try:
            base_lat, base_long =   float(self.DataSet.InternalData[0][self.DataSet.latestElement]), float(self.DataSet.InternalData[1][self.DataSet.latestElement])
            self.pan_lat, self.pan_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement] + self.panLocation[0]), float(self.DataSet.InternalData[1][self.DataSet.latestElement]  + self.panLocation[1])
        except:
            return

        self.axes.set_extent([base_lat - self.zoomScale ,base_lat + self.zoomScale ,base_long - self.zoomScale, base_long + self.zoomScale] ) # Zoom Scale
        
            #ccrs.PlateCarree()

        self.mapPlotting()


        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    MainWindow = MainWidget()

    MainWindow.show()

    sys.exit(app.exec())

