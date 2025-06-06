# Electron Ground station Tracker
This GUI aims to convert the pyside6 based ground station GUI used from 2023-2024 into an Electron based GUI from 2025 onwards.

# Description

The GUI is intended to display telemetry data from a rocket launch. This is done by monitoring a serial port with a radio connected and parsing the data sent in from this serial port (as a comma separated string). This data gets filtered and stored in a internal flask server on the backend. The frontend Electron program will then periodically requests this data and render it.

<a href="https://ibb.co/zhGWKVn0"><img src="https://i.ibb.co/KjFcCx03/GUI-V1-01.png" alt="GUI-V1-01" border="0"></a>
<sub><sup> V1.01 Dashboard Demo </sup></sub> 

# Getting Started

**Note**: If contributing or developing this project , see README in 'DOCUMENTATION' folder instead:
### Installation

Production Build (Note: Windows only) - Available in “Releases” on the right sidebar in the repository:

1. Download and extract Zip file from the latest release
2. Start GUI by opening **gsGUI.exe** file

### Setup (With Radio)

To Run the GUI once opened:

1. (Radio Setup) Connect a radio receiver to any serial port on your computer
    1. Find the serial port name that the device is connected to (via Device Manager)
    2. Enter the number of the port on the top left panel in the GUI (ex 4 if port id is COM4)
    3. Click the radio connection button, if “Radio Status:” on the top right status panel shows “connected” for more than 2-3 seconds then setup is correct
    4. **Note:** the radio should be configured to output comma separated values [specified in this repo](https://github.com/Ryerson-Rocketry/Library-RRC-encoder)
2. Enter the latitude and longitude of expected initial launch point of rocket (will be used as the starting camera location and map marker on the gps map)
3. Click “Enter Dashboard”

**If GUI is to be used offline:**
4. Within the map shown on the left in the dashboard, press the bottommost "+" button on the top left to save the map tiles near the currently zoomed in location. This will save them locally for use if host laptop/computer has no WIFI/data.

  
### Demo Setup (Without radio as well as pre-set Demo data)

- Simply press “Demo Mode” and “Click Enter Dashboard”
	- Demo data automatically included within the installation


# Roadmap (Updated: 2025-06-06)
### QOL
- Reformat starting screen (hidden menu on left to contain parameter setup and other)
- Add instructions manual on settings page and more comprehensive settings options
	- Additional options to be added:
		- GUI update timing: Specify the interval between each request to backend for new data to render
		- Data Purge: Purge all or selected data stored in backend collected from radio
- Add option to save starting parameters as new default on application start-up
### Frontend
- For https://github.com/Ryerson-Rocketry/Rocket-Antenna-Tracker integration:
	- Additional 3D Graph to display rocket current and predicted trajectory on 3 axis's centred on rocket launch point
	- Additional raw data readout for rocket azimuth
- Higher resolution backup map image for launch site map (for use if OSM map fails in offline use)
- GPS map: Add lines connecting each 

### Frontend and Backend
- SQLite integration
	- Record all data from the current launch session and save them to a locally hosted DB
	- Provide ability to replay this data at a later time

### Misc
- Allow data headers to be prespecified from a config file (instead of being hardcoded)
- Refactor frontend code
- Add more technical documentation

# Built With

### Software Stack:
- [Electron](https://www.electronjs.org/): Frontend desktop application framework
	- [Electron React Boilerplate](https://electron-react-boilerplate.js.org)(Tool): Boilerplate setup with react pre-integrated
	- [Axios](https://www.npmjs.com/package/axios)(Library): HTTP client for interfacing between internal Flask server and the Electron application
	- [React](https://react.dev)(Library): 
	- [Material UI](https://mui.com/material-ui/)(Library): Ready made UI component library for use with React
	- [Material UI X](https://mui.com/x/)(Library): Ready made graphing library for use with React
	- [Leaflet](https://leafletjs.com/)(Library): Open source interactive mapping library
- [Flask](https://electron-react-boilerplate.js.org): Backend Python web server framework
	- [PyInstaller](https://pyinstaller.org/en/stable/)(Tool): Python Application Packaging Tool
	- [Pyserial](https://pypi.org/project/pyserial/)(Library): Python serial port interface library

### Languages:
- Python: Used by backend
- JavaScript/html/CSS: Used by frontend