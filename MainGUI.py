# MainGUI.py
import sys
from PySide6 import QtCore, QtWidgets
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Graph
import DataRead
import MainWindow
from Trajectory import Trajectory

class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("Rocketry Ground Station GUI")
        self.resize(1800, 800)

        # Graph & Map & Other Widget Class Init ---
        self.DataSet = DataRead.DataTrack()
        self.trajectory = Trajectory()  # Initialize the Trajectory class

        self.dataPlots = []
        for i in range(4):
            self.dataPlots.append(Matplot())
            self.dataPlots[i].InitGraph("Time", self.DataSet.graphDict[i + 3], self.DataSet.graphDict[i + 3] + "-Time Graph")
            self.dataPlots[i].graphIndex = i + 3

        self.Map = Map(self.DataSet)
        self.mapState = False
        self.graphState = False

        # Graph & Map Class Init ---

        self.mainWindowUI = MainWindow.mainWindowUI()
        self.mainWindowUI.setup(self)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(self.mainWindowUI.layoutMain)
        self.setCentralWidget(widget)

        # Signals
        self.mainWindowUI.buttonLeft.clicked.connect(self.buttonLeftInteraction)
        self.mainWindowUI.threadUseButton.clicked.connect(self.threadUseCheck)

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

        self.mainWindowUI.plotTrajectoryButton.clicked.connect(self.plot_trajectory)  # Connect the plot trajectory button

    @QtCore.Slot()
    def plot_trajectory(self):
        self.Map.plot_trajectory(self.trajectory.parsed_data_df)

    # Slots

    @QtCore.Slot()
    def mapZoom(self, zoomlevel):
        self.Map.mapZoom(zoomlevel, self.DataSet)
        self.Map.draw()

    @QtCore.Slot()
    def mapPan(self, panType):
        self.Map.mapPan(panType, self.DataSet)
        self.Map.draw()

    @QtCore.Slot()  # Tab switching
    def tabSwitching(self, tabNum):
        self.DataSet.currentGraphTab = tabNum
        print(tabNum)  # debug
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
        def execute():
            while True:
                while self.graphState == True:
                    self.DataSet.maprunning = True
                    i = self.DataSet.latestElement
                    self.Map.mapPlotting()
                    self.Map.draw()
                    self.mainWindowUI.label1.setText("Acceleration:" + str(self.DataSet.InternalData[2][i]))
                    self.mainWindowUI.label2.setText("Pressure:" + str(self.DataSet.InternalData[3][i]))
                    self.DataSet.maprunning = False
                    self.graphState = False
                    self.mapState = True
                time.sleep(0.1)

        def execute2():
            while True:
                while self.mapState == True:
                    for i in range(len(self.dataPlots)):
                        self.dataPlots[i].plotPoint(self.DataSet, i)
                    self.mapState = False
                time.sleep(0.1)

        def execute3():
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
    def __init__(self):
        super(Matplot, self).__init__(Figure())
        self.figure = Figure()
        self.canvas = Graph(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.graphIndex = 0

    def InitGraph(self, xlabel, ylabel, title):
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)

    def redrawGraph(self, DataSet):
        i = DataSet.latestElement - 1
        for x in range(DataSet.latestElement - 1):
            self.axes.scatter(float(DataSet.InternalData[2][x]), float(DataSet.InternalData[DataSet.currentGraphTab][x]))

    def plotPoint(self, DataSet, graphIndex):
        i = DataSet.latestElement - 1
        if (DataSet.tolerance(graphIndex) == False):
            self.axes.scatter(float(DataSet.InternalData[2][i]), float(DataSet.InternalData[self.graphIndex][i]))
            self.draw()

class Map(Graph):
    def __init__(self, DataSet):
        super(Map, self).__init__()
        self.zoomScale = 1.0
        self.panLocation = [0.0, 0.0]
        self.pan_lat = 0.0
        self.pan_long = 0.0
        self.DataSet = DataSet
        self.figure = plt.figure()
        self.canvas = Graph(self.figure)
        self.axe = self.figure.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.initMap()

    def initMap(self):
        self.axes = plt.axes(projection=ccrs.PlateCarree())
        self.axes.coastlines()
        self.axes.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        self.axes.add_feature(cfeature.LAKES)
        self.axes.add_feature(cfeature.RIVERS)
        self.axes.add_feature(cfeature.OCEAN)
        self.axes.add_feature(cfeature.LAND)
        self.axes.add_feature(cfeature.BORDERS)

    def mapPlotting(self):
        self.figure.clear()
        base_lat, base_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement]), float(
            self.DataSet.InternalData[1][self.DataSet.latestElement])
        self.pan_lat, self.pan_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement]) + self.panLocation[
            0], float(self.DataSet.InternalData[1][self.DataSet.latestElement]) + self.panLocation[1]
        self.initMap()
        self.mapZoom()
        self.axes.set_extent(
            [base_lat - self.zoomScale, base_lat + self.zoomScale, base_long - self.zoomScale, base_long + self.zoomScale])
        self.axes.plot(base_lat, base_long, color='blue', linewidth='2', marker='o')
        self.axes.plot(self.pan_lat, self.pan_long, color='red', linewidth='3', marker='x')
        self.axes.plot(-79.38, 43.65, color='red', linewidth='2', marker='o')
        self.axes.text(-79.48, 43.75, "Launch Point")

    def mapZoom(self):
        self.zoomScale = abs(-79.48 - (self.DataSet.InternalData[0][self.DataSet.latestElement]) + 0.5)
        print(self.zoomScale)

    def mapPan(self, panType, dataSet):
        if dataSet.maprunning:
            return
        self.figure.clear()
        match (panType):
            case 1: self.panLocation[0] -= 0.5
            case 2: self.panLocation[0] += 0.5
            case 3: self.panLocation[1] += 0.5
            case 4: self.panLocation[1] -= 0.5
        base_lat, base_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement]), float(
            self.DataSet.InternalData[1][self.DataSet.latestElement])
        self.pan_lat, self.pan_long = float(self.DataSet.InternalData[0][self.DataSet.latestElement] +
                                            self.panLocation[0]), float(self.DataSet.InternalData[1][
                                                                            self.DataSet.latestElement] +
                                                                            self.panLocation[1])
        self.axes.set_extent(
            [base_lat - self.zoomScale, base_lat + self.zoomScale, base_long - self.zoomScale, base_long + self.zoomScale])
        self.mapPlotting()

    def plot_trajectory(self, data):
        self.figure.clear()
        self.initMap()
        self.axes.set_global()
        lons = data['longitude'].values
        lats = data['latitude'].values
        self.axes.plot(lons, lats, marker='o', color='r', transform=ccrs.Geodetic())
        self.axes.set_title('Trajectory on World Map')
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow = MainWidget()
    MainWindow.show()
    sys.exit(app.exec())
