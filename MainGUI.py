import sys
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore
import PySide6.QtWidgets

import time
import numpy

#Map dependency
from matplotlib import pyplot as plt
import scipy

#Graph dependency
from matplotlib.figure import Figure

#For handling backend use of matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Graph

import cartopy.crs as ccrs
import cartopy.feature as cfeature




import DataRead

class MainWidget(QtWidgets.QMainWindow): #Class for general UI stuff (buttons and text)
    def __init__(self):
        super(MainWidget, self).__init__()

        self.setWindowTitle("Test Dot Mover")
        self.resize(1800,800)

        self.label1 = QtWidgets.QLabel()
        self.label1.setText("Acceleration: 0")
        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Pressure: 0")
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("Placeholder: 0")
        self.label4 = QtWidgets.QLabel()
        self.label4.setText("Placeholder: 0")

        self.buttonRight = QtWidgets.QPushButton()
        self.buttonRight.setText("Preset Coordinate List")
        self.buttonLeft = QtWidgets.QPushButton()
        self.buttonLeft.setText("Live Update")
        

        #Graphical -------

        #Graph & Map ---

        self.DataPlot = Matplot() 
        self.Map = Map()

        #Graph ---
        
        """
        #Painter Instance
        #self.map = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("GTAAREA.jpg")) #A graphical object that takes in a pixelmap object

        self.dot = QtWidgets.QGraphicsRectItem() #A graphical object
        self.dot.setRect(10,10,10,10)

        self.scene = QtWidgets.QGraphicsScene() #Scene object that contains graphical object
        #self.scene.addItem(self.map)
        self.scene.addItem(self.dot)

        self.view = QtWidgets.QGraphicsView(self.scene) #A object (window) to show the scene
        self.view.setFixedWidth(1000)
        self.view.setFixedHeight(750)

        """

        #creates an object for a grid type window layout, above objects can be added to the layout
        dataLayout = QtWidgets.QGridLayout() 
        dataLayout.addWidget(self.DataPlot, 0, 0, 1 , 4) 
        


        dataChildLayout = QtWidgets.QVBoxLayout()
        

        dataChildLayout.addWidget(self.label1) 
        dataChildLayout.addWidget(self.label2)
        dataChildLayout.addWidget(self.label3)
        dataChildLayout.addWidget(self.label4)

        dataLayout.addLayout(dataChildLayout,1,0)
        dataLayout.addWidget(self.buttonLeft, 2 ,1)
        dataLayout.addWidget(self.buttonRight, 2 ,2)
        

        

        widget = QtWidgets.QWidget(self)
        

        layoutMain = QtWidgets.QGridLayout()
        layoutMain.addWidget(self.Map, 0,0,8,3) #to be contained in cell row:0,column:0, spanning 1 row and 3 columns
        layoutMain.addLayout(dataLayout, 0, 3, 1, 2)

        widget.setLayout(layoutMain)

        self.setCentralWidget(widget)
       

        self.buttonRight.clicked.connect(self.buttonRightInteraction) #when interacted with, executes function within the parameter
        self.buttonLeft.clicked.connect(self.buttonLeftInteraction) #when interacted with, executes function within the parameter


    

    @QtCore.Slot()
    def buttonLeftInteraction(self):
        

        DataSet = DataRead.Data() 
        
        Latest = DataRead.FileReadSequential(DataSet) #A 2D array for x,y coordinates

        
        
        #for i in range(13): #temporary, gonna make a while loop later and another button to terminate the file checking

        while True:

            QtCore.QCoreApplication.processEvents() #apparently a "bad" way to update the gui as the for loop progresses. Need to figure out how to use the built in Qthread/multithreading to do it properly

            i = DataSet.LatestElement -1
            
            #self.dot.setPos(float(DataSet.InternalData[2][i]),float(DataSet.InternalData[3][i])) #sets x and y from CoordinateArray
            

            
            self.DataPlot.axes.scatter(float(DataSet.InternalData[2][i]), float(DataSet.InternalData[3][i]))
            self.DataPlot.draw()

            self.Map.mapPlotting(DataSet)
            self.Map.draw()

            print (DataSet.InternalData[0][i] + "," + DataSet.InternalData[1][i]) #debug

            self.label1.setText("Acceleration:" + DataSet.InternalData[2][i])
            self.label2.setText("Pressure:" + DataSet.InternalData[3][i])

            Latest = DataRead.FileReadSequential(DataSet) #A 2D array for x,y coordinates

            
            

            time.sleep(1)
        
   
    @QtCore.Slot()
    def buttonRightInteraction(self):
        DataSet = DataRead.fileRead() #A 2D array for x,y coordinates

        for i in range(len(DataSet[0])):
            
            self.dot.setPos(float(DataSet[0][i]),float(DataSet[1][i])) #sets x and y from CoordinateArray
            print (DataSet[0][i] + "," + DataSet[1][i]) #debug

            #self.DataPlot.axes.clear()
            self.DataPlot.axes.scatter(float(DataSet[2][i]), float(DataSet[3][i]))
            self.DataPlot.draw()

            

            self.label1.setText("Placeholder:" + DataSet[2][i])
            self.label2.setText("Placeholder:" + DataSet[3][i] )



            QtCore.QCoreApplication.processEvents() #apparently a "bad" way to update the gui as the for loop progresses. Need to figure out how to use the built in Qthread/multithreading to do it properly

            time.sleep(1)


        

class Matplot(Graph):

    def __init__(self):
        super(Matplot, self).__init__(Figure())

        self.figure = Figure()
        self.canvas = Graph (self.figure)
        self.axes = self.figure.add_subplot(111) 

        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Placeholder")
        self.axes.set_title("Graph")

        #self.DataPlot.axes.clear() #Reset

class Map(Graph):
    def __init__(self):
        super(Map, self).__init__()

        self.figure = plt.figure()
        self.canvas = Graph (self.figure)
        self.axes = self.figure.add_subplot(1,1,1, projection = ccrs.PlateCarree())

        self.initMap() 

    def initMap(self): #Since main method of rendering the map is to draw , clear, and redraw the map, defined a function to do all of that easily
        self.axes = plt.axes(projection=ccrs.PlateCarree())
        self.axes.coastlines()
        
        self.axes.gridlines(draw_labels=True,dms = True,x_inline = False, y_inline = False) #grid and coordinate axises

        #ignore
        #self.axes.set_extent([-80.38 ,-74.38 ,30,64.65])
        #self.axes.stock_img()#scipy required, overlays a actual graphical image onto the map

        #graphical glitches when using the commented out code. Unsure why
        #self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'cultural', name= 'admin_0_boundary_lines_land', scale='10m', facecolor='black'))
        #self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'physical', name= 'land', scale='50m', facecolor='green'))
        self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'cultural', name= 'urban_areas', scale='10m', facecolor='grey'))
        #self.axes.add_feature(cfeature.NaturalEarthFeature(category= 'physical', name= 'rivers_lake_centerlines', scale='50m', facecolor='blue'))

        self.axes.add_feature(cfeature.LAKES)
        self.axes.add_feature(cfeature.RIVERS)
        self.axes.add_feature(cfeature.OCEAN)
        self.axes.add_feature(cfeature.LAND)
        self.axes.add_feature(cfeature.BORDERS)


    def mapPlotting(self,DataSet):

        self.figure.clear()

        base_lat, base_long =   float(DataSet.InternalData[0][DataSet.LatestElement - 1]), float(DataSet.InternalData[1][DataSet.LatestElement - 1])   #-79.38 , 43.65
        base_lat2, base_long2 =   float(DataSet.InternalData[0][0]), float(DataSet.InternalData[1][0])

        self.initMap()

        plt.plot([base_lat],[base_long], color = 'blue', linewidth = '2', marker= 'o')
        plt.text (base_lat2, base_long2, 'launch point', transform = ccrs.PlateCarree())
        plt.text (base_lat + 0.10, base_long - 0.20 , str(base_lat) + " " +  str(base_long), transform = ccrs.PlateCarree())

#class ActionThread ()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    MainWindow = MainWidget()



    
    MainWindow.show()


    sys.exit(app.exec())



