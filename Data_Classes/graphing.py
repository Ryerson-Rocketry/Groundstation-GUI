#Map dependency
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy #unused

#Graph dependency
from matplotlib.figure import Figure

#For handling backend use of matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Graph

LAUNCH_POINT_X = 0
LAUNCH_POINT_Y = 0

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
    def InitGraph (self, xlabel, ylabel, title, graph_index):
        self.x_string = xlabel
        self.y_string = ylabel
        self.title_string = title

        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)

        self.graph_index = graph_index + 3

    def plotPoint (self, DataSet, graphIndex):
        if (DataSet.tolerance(graphIndex) == False):
            self.axes.clear()
            
            #axis labels and titles need to be readded after graphs are cleared
            self.axes.set_xlabel(self.x_string)
            self.axes.set_ylabel(self.y_string)
            self.axes.set_title(self.title_string)
            
            self.axes.plot((DataSet.InternalData[2]), (DataSet.InternalData[self.graph_index]), marker='o', linewidth = 0.1, markersize = 2 )
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