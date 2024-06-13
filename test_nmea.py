import pandas as pd
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pynmea2
import time
import random
import threading
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def calculate_checksum(nmea_str):
    # Strip whitespace from the input string
    nmea_str = nmea_str.strip()
    
    # Remove the initial '$' if present
    if nmea_str[0] == "$":
        nmea_str = nmea_str[1:]
    
    try:
        # Split the NMEA string into data and the provided checksum
        dataset, checksum = nmea_str.split("*")
    except ValueError:
        return "ERROR: Invalid NMEA format"
    
    # Initialize the actual checksum calculation
    actual_checksum = 0

    # Calculate the checksum by XORing all characters in the dataset
    for data in dataset:
        actual_checksum ^= ord(data)
    
    # Convert the provided checksum to an integer
    provided_checksum = int(checksum, 16)
    
    # Compare the calculated checksum with the provided checksum
    if actual_checksum != provided_checksum:
        return "ERROR: Invalid checksum, degraded transmission integrity"
    
    # Return the calculated checksum in hexadecimal format
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

# Function to convert decimal degrees to degrees and decimal minutes
def decimal_to_dm(dec):
    degrees = int(dec)
    minutes = (dec - degrees) * 60
    return f"{degrees * 100 + minutes:.4f}"

# Function to generate new NMEA messages with correct checksums
def generate_nmea_message():
    lat = 34.5201 + random.uniform(-0.001, 0.001)
    lon = -118.1404 + random.uniform(-0.001, 0.001)
    alt = random.uniform(100.0, 600.0)
    timestamp = pd.Timestamp.now().strftime("%H%M%S.00")
    lat_dm = decimal_to_dm(lat)
    lon_dm = decimal_to_dm(-lon)  # Convert to positive for NMEA format
    
    nmea_message = f"GPGGA,{timestamp},{lat_dm},N,{lon_dm},W,1,08,0.9,{alt:.1f},M,0.0,M,,"
    
    # Calculate checksum
    checksum = 0
    for char in nmea_message:
        checksum ^= ord(char)
    checksum_str = f"*{checksum:02X}"
    
    # Complete the NMEA message
    complete_message = f"${nmea_message}{checksum_str}"
    return complete_message

# Initialize an empty DataFrame to store parsed data
parsed_data_df = pd.DataFrame(columns=['latitude', 'longitude', 'altitude', 'timestamp'])

# Initialize the GUI
app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMEA Processor")

        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.ax = self.canvas.figure.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.plot_button = QPushButton("Plot Trajectory")
        self.plot_button.clicked.connect(self.plot_trajectory)
        layout.addWidget(self.plot_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

            self.ax.set_title('Trajectory on World Map')
            self.canvas.draw()

window = MainWindow()
window.show()

def process_stream():
    global parsed_data_df
    while True:
        nmea_message = generate_nmea_message()
        parsed_data = parse_nmea_message(nmea_message)
        if parsed_data:
            # Create a DataFrame from the parsed data
            new_data_df = pd.DataFrame([parsed_data])
            # Concatenate the new data to the existing DataFrame
            parsed_data_df = pd.concat([parsed_data_df, new_data_df], ignore_index=True)
        time.sleep(1)  # Simulate a delay between incoming messages

# Start the data stream processing in a separate thread
stream_thread = threading.Thread(target=process_stream)
stream_thread.daemon = True
stream_thread.start()

app.exec()
