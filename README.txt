Groundstation - GUI
A GUI based on Python Pyside Library

This GUI application utilizes Python Pyside, matplotlib, and Cartopy to generate GUI windows, graphs, and maps based off of sensor data and GPS coordinates.

The specifications of the GUI application are: to deliver a GUI which displays current rocket location and graphs on sensor data such as battery voltage, temperature, pressure, etc. using live data.
Panning and scaling of the map is automatic, and should always keep in frame both the launch point and the current rocket location. 
This live data is fed via a common .csv file, in which the radio continually appends new live data to the last line of the .csv file. 

The GUI application is formulated into three main files: MainGUI.py, MainWindow.py, and DataRead.py. 

MainWindow.py formulates the main graph window that is used in the GUI. It allocates a partition of the GUI window space, and allocates space for the respective sensor data graphs with labels by manual selection of cells. 

DataRead.py is the general data-reading class; it takes in last line input from the .csv file and partitions it into arrays of usable data, which are parsed to the graphs and map for display.

MainGUI.py is the main GUI window application, which invokes the GUI application. It allocates space for and displays the Cartopy-based library map, while setting panning and scaling parameters. 
The map is populated with the most recent rocket location with the launch point in view at all times.
It also sets a manual panning option, which can be used via left button interaction
Additionally, it invokes MainWindow.py, which allocates space for the graphs with sensor data. Additional methods in MainGUI.py populate the graphs with data.
These graphs are displayed separately; one must switch "tabs" in order to see the respective desired graphs.
This implementation allows for minimalistic design and computational complexity; not all graphs need to be parsed, displayed and loaded at the same time with data. 





