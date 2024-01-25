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

class MainWidget(QtWidgets.QMainWindow): #Main Class
    def __init__(self):
        super(MainWidget, self).__init__()

        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("Rocketry Ground Station GUI")
        self.resize(1800,800)

        self.label1 = QtWidgets.QLabel()
        self.label1.setText("Acceleration: 0")
        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Pressure: 0")
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("Placeholder: 0")
        self.label4 = QtWidgets.QLabel()
        self.label4.setText("Current Qthread Usage: 1/16")
        
        self.buttonLeft = QtWidgets.QPushButton()
        self.buttonLeft.setText("Start")

        self.buttonZoomIn = Button("+")
        self.buttonZoomOut = Button("-")

        #Graph & Map & Other Widget Class Init ---

        self.DataPlot1 = Matplot() 
        self.DataPlot1.InitGraph("Time", "Pressure", "Pressure-Time Graph")

        self.DataSet = DataRead.DataTrack()
        self.Map = Map(self.DataSet)   
        self.mapState = False

        self.tabButton1 = Button("Pressure:")
        self.tabButton2 = Button("Temperature:")
        self.tabButton3 = Button("Signal Strength:")
        self.tabButton4 = Button("Battery Voltage:")

        self.threadUseButton = Button("Check Qthread Usage")

        #Graph & Map Class Init ---
        
        #Layouts ---
        tabLayout = QtWidgets.QHBoxLayout()
        tabLayout.addWidget(self.tabButton1)
        tabLayout.addWidget(self.tabButton2)
        tabLayout.addWidget(self.tabButton3)
        tabLayout.addWidget(self.tabButton4)

        #creates an object for a grid type window layout, above objects can be added to the layout
        self.dataLayout = QtWidgets.QGridLayout() 
        self.dataLayout.addWidget(self.DataPlot1, 2, 0, 1 , 4) 
        
        dataChildLayout = QtWidgets.QVBoxLayout()
        
        dataChildLayout.addWidget(self.label1) 
        dataChildLayout.addWidget(self.label2)
        dataChildLayout.addWidget(self.label3)
        dataChildLayout.addWidget(self.label4)

        self.dataLayout.addLayout(tabLayout,1,0)
        self.dataLayout.addLayout(dataChildLayout,3,0)
        self.dataLayout.addWidget(self.buttonLeft, 4 ,0)
        self.dataLayout.addWidget(self.threadUseButton, 4, 1)
    
        widget = QtWidgets.QWidget(self)
        
        layoutMain = QtWidgets.QGridLayout()
        layoutMain.addWidget(self.Map, 0,0,8,3) #to be contained in cell row:0,column:0, spanning 8 row and 3 columns
        layoutMain.addWidget(self.buttonZoomIn, 9,0,1,1)
        layoutMain.addWidget(self.buttonZoomOut, 9,1,1,1)
        layoutMain.addLayout(self.dataLayout, 1, 3, 1, 2)

        widget.setLayout(layoutMain)
        self.setCentralWidget(widget)
       
        #Signals
        self.buttonLeft.clicked.connect(self.buttonLeftInteraction) 
        self.threadUseButton.clicked.connect(self.threadUseCheck) 

        self.tabButton1.clicked.connect(lambda x: self.tabSwitching(3))
        self.tabButton2.clicked.connect(lambda x: self.tabSwitching(4))
        self.tabButton3.clicked.connect(lambda x: self.tabSwitching(5))
        self.tabButton4.clicked.connect(lambda x: self.tabSwitching(6))

        self.buttonZoomIn.clicked.connect(lambda x: self.mapZoom(1))
        self.buttonZoomOut.clicked.connect(lambda x: self.mapZoom(2))
    

    #Slots 
    @QtCore.Slot()    
    def mapZoom(self, zoomlevel):
        self.Map.mapZoom(zoomlevel)
        self.Map.draw()

    @QtCore.Slot() #Tab switching
    def tabSwitching(self, tabNum):
        self.DataSet.currentGraphTab = tabNum
        print (tabNum) #debug 

        self.DataSet.changedState = True

        
    @QtCore.Slot()
    def threadUseCheck(self):

        def execute():
            self.label4.setText("Current Qthread Usage: " + str(self.threadpool.activeThreadCount()) + "/16")

        thread = WorkerThread(execute)
        self.threadpool.start(thread)
    
    @QtCore.Slot()
    def buttonLeftInteraction(self):    

        def execute(): #map thread
            DataRead.FileReadSequential(self.DataSet) #Needed to get the latest data points in the datafile
            
            while True:
                i = self.DataSet.latestElement -1

                self.Map.mapPlotting()
                self.Map.draw()
                
                print (self.DataSet.InternalData[0][i] + "," + self.DataSet.InternalData[1][i]) #debug

                self.label1.setText("Acceleration:" + self.DataSet.InternalData[2][i])
                self.label2.setText("Pressure:" + self.DataSet.InternalData[3][i])

                DataRead.FileReadSequential(self.DataSet)   
                
                self.mapState = True #tells the graph thread that it can plot

                time.sleep(1)               

        def execute2(): #graph thread
            DataRead.FileReadSequential(self.DataSet) #Needed to get the latest data points in the datafile
                
            while True:

                if (self.DataSet.changedState == True): #replots a new graph anytime a new tab (with new data types) is pressed

                    self.DataSet.changedState = False
                    self.DataPlot1.axes.clear()
                    self.DataPlot1.InitGraph("Time", self.DataSet.graphDict[self.DataSet.currentGraphTab], self.DataSet.graphDict[self.DataSet.currentGraphTab] + "-Time Graph")
                    self.DataPlot1.redrawGraph(self.DataSet)

                while self.mapState == True: #only plots after the map has plotted to maintain syncronization    

                    self.DataPlot1.plotPoint(self.DataSet)
                    self.mapState = False

                time.sleep(0.01)

        #Seperates the above executed code into two seperate thread, consequently the main thread (and window) won't go unresponsive as well as the graph being able to update independently of the map
        thread = WorkerThread(execute)
        thread2 = WorkerThread(execute2) 
        self.threadpool.start(thread)
        self.threadpool.start(thread2)

        
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

    #Defines graph axes
    def InitGraph (self, xlabel, ylabel, title):
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)

    #plots all points up to the latest element in the dataset
    def redrawGraph (self, DataSet):
        i = DataSet.latestElement - 1
        for x in range (DataSet.latestElement - 1):
            self.axes.scatter(float(DataSet.InternalData[2][x]), float(DataSet.InternalData[DataSet.currentGraphTab][x]))
        self.draw()

    def plotPoint (self, DataSet):

        i = DataSet.latestElement - 1

        self.axes.scatter(float(DataSet.InternalData[2][i]), float(DataSet.InternalData[DataSet.currentGraphTab][i]), )
        self.draw()


class Map(Graph):
    def __init__(self, DataSet):
        super(Map, self).__init__()
        self.zoomScale = 2.5 #initial zoom

        self.DataSet = DataSet
        self.figure = plt.figure()
        self.canvas = Graph (self.figure)
        self.axes = self.figure.add_subplot(1,1,1, projection = ccrs.PlateCarree())

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

        base_lat, base_long =   float(self.DataSet.InternalData[0][self.DataSet.latestElement - 1]), float(self.DataSet.InternalData[1][self.DataSet.latestElement - 1])   #-79.38 , 43.65
        base_lat2, base_long2 =   float(self.DataSet.InternalData[0][0]), float(self.DataSet.InternalData[1][0])

        self.initMap()

        plt.plot([base_lat],[base_long], color = 'blue', linewidth = '2', marker= 'o')
        self.axes.set_extent([base_lat - self.zoomScale ,base_lat + self.zoomScale ,base_long - self.zoomScale, base_long + self.zoomScale])
        plt.text (base_lat + 0.010, base_long - 0.020 , str(base_lat) + " " +  str(base_long), transform = ccrs.PlateCarree())

    def mapZoom(self, zoomType):
        
        if (zoomType == 1):
            self.zoomScale = self.zoomScale + 0.25;
         
        if (self.zoomScale <= 0.25):
            return
       
        if (zoomType == 2):
                self.zoomScale = self.zoomScale - 0.25;
        
        self.figure.clear()
    
        base_lat, base_long =   float(self.DataSet.InternalData[0][self.DataSet.latestElement - 1]), float(self.DataSet.InternalData[1][self.DataSet.latestElement - 1])
        
        self.initMap()

        plt.plot([base_lat],[base_long], color = 'blue', linewidth = '2', marker= 'o')
        plt.text (base_lat + 0.010, base_long - 0.020 , str(base_lat) + " " +  str(base_long), transform = ccrs.PlateCarree())

        plt.draw()
        self.axes.set_extent([base_lat - self.zoomScale ,base_lat + self.zoomScale ,base_long - self.zoomScale, base_long + self.zoomScale], ccrs.PlateCarree())
        
class Button (QtWidgets.QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        
        self.setText(text)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    MainWindow = MainWidget()

    MainWindow.show()

    sys.exit(app.exec())



