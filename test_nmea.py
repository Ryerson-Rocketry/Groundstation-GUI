import pandas as pd
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal, Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pynmea2
import time
import random
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def calculate_checksum(nmea_str):
    nmea_str = nmea_str.strip()
    if nmea_str[0] == "$":
        nmea_str = nmea_str[1:]
    try:
        dataset, checksum = nmea_str.split("*")
    except ValueError:
        return "ERROR: Invalid NMEA format"
    actual_checksum = 0
    for data in dataset:
        actual_checksum ^= ord(data)
    provided_checksum = int(checksum, 16)
    if actual_checksum != provided_checksum:
        return "ERROR: Invalid checksum, degraded transmission integrity"
    calculated_checksum = '{:02X}'.format(actual_checksum)
    print("Accurate")
    return calculated_checksum

def parse_nmea_message(nmea_str):
    try:
        msg = pynmea2.parse(nmea_str)
        if isinstance(msg, pynmea2.types.talker.GGA):
            return {
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude,
                'timestamp': msg.timestamp
            }
        else:
            return None
    except (pynmea2.ParseError, pynmea2.ChecksumError) as e:
        print(f"Error parsing NMEA message: {e}")
        return None

def pre_process(data):
    data = data.dropna()
    return data

def decimal_to_dm(dec):
    degrees = int(dec)
    minutes = (dec - degrees) * 60
    return f"{degrees * 100 + minutes:.4f}"

def generate_nmea_message():
    lat = 34.5201 + random.uniform(-0.1, 0.1)
    lon = -118.1404 + random.uniform(-0.1, 0.1)
    alt = random.uniform(100.0, 600.0)
    timestamp = pd.Timestamp.now().strftime("%H%M%S.00")
    lat_dm = decimal_to_dm(lat)
    lon_dm = decimal_to_dm(-lon)
    
    nmea_message = f"GPGGA,{timestamp},{lat_dm},N,{lon_dm},W,1,08,0.9,{alt:.1f},M,0.0,M,,"
    
    checksum = 0
    for char in nmea_message:
        checksum ^= ord(char)
    checksum_str = f"*{checksum:02X}"
    
    complete_message = f"${nmea_message}{checksum_str}"
    return complete_message

class DataStreamThread(QThread):
    new_data = Signal(dict)

    def __init__(self):
        super().__init__()
        self._running = False

    def run(self):
        global parsed_data_df
        while self._running:
            nmea_message = generate_nmea_message()
            parsed_data = parse_nmea_message(nmea_message)
            if parsed_data:
                self.new_data.emit(parsed_data)
            time.sleep(1)

    def start_stream(self):
        self._running = True
        self.start()

    def stop_stream(self):
        self._running = False
        self.wait()

parsed_data_df = pd.DataFrame(columns=['latitude', 'longitude', 'altitude', 'timestamp'])

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMEA Processor")

        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.ax = self.canvas.figure.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Trajectory")
        self.start_button.clicked.connect(self.start_trajectory)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Trajectory")
        self.stop_button.clicked.connect(self.stop_trajectory)
        button_layout.addWidget(self.stop_button)
        
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        button_layout.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        button_layout.addWidget(self.zoom_out_button)
        
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.current_extent = None
        self.data_stream_thread = DataStreamThread()
        self.data_stream_thread.new_data.connect(self.update_data)

    @Slot(dict)
    def update_data(self, parsed_data):
        global parsed_data_df
        new_data_df = pd.DataFrame([parsed_data])
        parsed_data_df = pd.concat([parsed_data_df, new_data_df], ignore_index=True)
        self.plot_trajectory()

    def plot_trajectory(self):
        global parsed_data_df
        if not parsed_data_df.empty:
            preprocessed_data = pre_process(parsed_data_df)
            self.ax.clear()
            self.ax.coastlines()
            self.ax.add_feature(cfeature.BORDERS)
            self.ax.set_global()

            lons = preprocessed_data['longitude'].values
            lats = preprocessed_data['latitude'].values
            self.ax.plot(lons, lats, marker='o', color='r', transform=ccrs.Geodetic())

            if self.current_extent is None:
                min_lat = lats.min() - 0.5
                max_lat = lats.max() + 0.5
                min_lon = lons.min() - 0.5
                max_lon = lons.max() + 0.5
                self.current_extent = [min_lon, max_lon, min_lat, max_lat]

            self.ax.set_extent(self.current_extent, crs=ccrs.PlateCarree())

            self.ax.set_title('Trajectory on World Map')
            self.canvas.draw()

    def start_trajectory(self):
        self.data_stream_thread.start_stream()

    def stop_trajectory(self):
        self.data_stream_thread.stop_stream()

    def zoom_in(self):
        if self.current_extent:
            self.current_extent = [
                self.current_extent[0] + 0.1,
                self.current_extent[1] - 0.1,
                self.current_extent[2] + 0.1,
                self.current_extent[3] - 0.1,
            ]
            self.ax.set_extent(self.current_extent, crs=ccrs.PlateCarree())
            self.canvas.draw()

    def zoom_out(self):
        if self.current_extent:
            self.current_extent = [
                self.current_extent[0] - 0.1,
                self.current_extent[1] + 0.1,
                self.current_extent[2] - 0.1,
                self.current_extent[3] + 0.1,
            ]
            self.ax.set_extent(self.current_extent, crs=ccrs.PlateCarree())
            self.canvas.draw()

window = MainWindow()
window.show()

app.exec()
