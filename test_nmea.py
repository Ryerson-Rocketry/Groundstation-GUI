import pandas as pd
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal, Slot, Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pynmea2
import time
import random
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class KalmanFilter:
    def __init__(self, dt, u_noise, s_noise):
        self.dt = dt
        self.u_noise = u_noise
        self.s_noise = s_noise
        self.A = np.array([[1, dt], [0, 1]])  # State transition matrix
        self.B = np.array([0.5*dt**2, dt]).reshape(2, 1)  # Control input matrix
        self.H = np.array([1, 0]).reshape(1, 2)  # Observation matrix
        self.P = np.eye(2)  # Initial estimate covariance
        self.R = np.eye(1) * self.s_noise  # Measurement noise covariance
        self.Q = np.eye(2) * self.u_noise  # Process noise covariance
        self.x = np.zeros((2, 1))  # Initial state estimate

    def predict(self, u=0):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(self.H, self.P))

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

# Initial conditions for the rocket launch simulation
initial_lat = 28.5721  # Example: Kennedy Space Center
initial_lon = -80.6480
initial_alt = 0.0
velocity = 0.05  # Change in degrees per second, example value
altitude_increase = 50  # Meters per second, example value

def generate_nmea_message():
    global initial_lat, initial_lon, initial_alt, velocity, altitude_increase
    
    # Simulate the rocket ascent
    initial_lat += velocity * random.uniform(0.9, 1.1)  # Adding some variation
    initial_lon += velocity * random.uniform(0.9, 1.1)
    initial_alt += altitude_increase * random.uniform(0.9, 1.1)
    
    timestamp = pd.Timestamp.now().strftime("%H%M%S.00")
    lat_dm = decimal_to_dm(initial_lat)
    lon_dm = decimal_to_dm(-initial_lon)  # Convert to positive for NMEA format
    
    nmea_message = f"GPGGA,{timestamp},{lat_dm},N,{lon_dm},W,1,08,0.9,{initial_alt:.1f},M,0.0,M,,"
    
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
        self.discard_data = False

    def run(self):
        global parsed_data_df
        while self._running:
            nmea_message = generate_nmea_message()
            parsed_data = parse_nmea_message(nmea_message)
            if parsed_data and not self.discard_data:
                self.new_data.emit(parsed_data)
            time.sleep(1)

    def start_stream(self):
        self._running = True
        self.discard_data = False
        self.start()

    def stop_stream(self):
        self._running = False
        self.wait()

    def discard_incoming_data(self):
        self.discard_data = True

    def allow_incoming_data(self):
        self.discard_data = False

parsed_data_df = pd.DataFrame(columns=['latitude', 'longitude', 'altitude', 'timestamp'])
kalman_filter_data = pd.DataFrame(columns=['latitude', 'longitude', 'altitude', 'timestamp'])
kalman_filters = {
    'latitude': KalmanFilter(dt=1, u_noise=0.001, s_noise=0.001),
    'longitude': KalmanFilter(dt=1, u_noise=0.001, s_noise=0.001)
}
last_data_time = time.time()
using_kalman_filter = False
kalman_filter_running = False
predicted_data_point = None

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
        
        self.cut_stream_button = QPushButton("Cut Data Stream")
        self.cut_stream_button.clicked.connect(self.cut_data_stream)
        button_layout.addWidget(self.cut_stream_button)
        
        self.resume_stream_button = QPushButton("Resume Data Stream")
        self.resume_stream_button.clicked.connect(self.resume_data_stream)
        button_layout.addWidget(self.resume_stream_button)
        
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

        self.kalman_timer = QTimer()
        self.kalman_timer.timeout.connect(self.update_kalman_filter)

    @Slot(dict)
    def update_data(self, parsed_data):
        global parsed_data_df, last_data_time, using_kalman_filter, predicted_data_point
        new_data_df = pd.DataFrame([parsed_data])
        parsed_data_df = pd.concat([parsed_data_df, new_data_df], ignore_index=True)

        for coord in ['latitude', 'longitude']:
            kalman_filters[coord].predict()
            kalman_filters[coord].update(parsed_data[coord])
            parsed_data[coord] = kalman_filters[coord].x[0, 0]

        last_data_time = time.time()
        using_kalman_filter = False
        predicted_data_point = None  # Reset the predicted data point when new data arrives
        self.plot_trajectory()

    @Slot()
    def plot_trajectory(self):
        global parsed_data_df, kalman_filter_data, using_kalman_filter, predicted_data_point

        self.ax.clear()
        self.ax.coastlines()
        self.ax.add_feature(cfeature.BORDERS)
        self.ax.set_global()

        preprocessed_data = None
        preprocessed_kalman_data = None

        if not parsed_data_df.empty:
            preprocessed_data = pre_process(parsed_data_df)
            lons = preprocessed_data['longitude'].values
            lats = preprocessed_data['latitude'].values
            self.ax.plot(lons, lats, marker='o', color='r', transform=ccrs.Geodetic())

        if not kalman_filter_data.empty:
            preprocessed_kalman_data = pre_process(kalman_filter_data)
            kalman_lons = preprocessed_kalman_data['longitude'].values
            kalman_lats = preprocessed_kalman_data['latitude'].values

            # Plot the Kalman filter points but only connect to the last data point
            if using_kalman_filter:
                self.ax.plot([preprocessed_data['longitude'].values[-1], kalman_lons[0]],
                             [preprocessed_data['latitude'].values[-1], kalman_lats[0]],
                             marker='o', color='g', transform=ccrs.Geodetic())
                if len(kalman_lons) > 1:
                    self.ax.plot(kalman_lons[1:], kalman_lats[1:], marker='o', color='g', transform=ccrs.Geodetic())
            else:
                self.ax.plot(kalman_lons, kalman_lats, marker='o', color='g', transform=ccrs.Geodetic())

        if self.current_extent is None:
            if preprocessed_data is not None and preprocessed_kalman_data is not None:
                min_lat = min(preprocessed_data['latitude'].min(), preprocessed_kalman_data['latitude'].min()) - 0.5
                max_lat = max(preprocessed_data['latitude'].max(), preprocessed_kalman_data['latitude'].max()) + 0.5
                min_lon = min(preprocessed_data['longitude'].min(), preprocessed_kalman_data['longitude'].min()) - 0.5
                max_lon = max(preprocessed_data['longitude'].max(), preprocessed_kalman_data['longitude'].max()) + 0.5
            elif preprocessed_data is not None:
                min_lat = preprocessed_data['latitude'].min() - 0.5
                max_lat = preprocessed_data['latitude'].max() + 0.5
                min_lon = preprocessed_data['longitude'].min() - 0.5
                max_lon = preprocessed_data['longitude'].max() + 0.5
            elif preprocessed_kalman_data is not None:
                min_lat = preprocessed_kalman_data['latitude'].min() - 0.5
                max_lat = preprocessed_kalman_data['latitude'].max() + 0.5
                min_lon = preprocessed_kalman_data['longitude'].min() - 0.5
                max_lon = preprocessed_kalman_data['longitude'].max() + 0.5
            self.current_extent = [min_lon, max_lon, min_lat, max_lat]
        else:
            if preprocessed_data is not None:
                new_min_lat = preprocessed_data['latitude'].min() - 0.5
                new_max_lat = preprocessed_data['latitude'].max() + 0.5
                new_min_lon = preprocessed_data['longitude'].min() - 0.5
                new_max_lon = preprocessed_data['longitude'].max() + 0.5
                self.current_extent = [
                    min(self.current_extent[0], new_min_lon),
                    max(self.current_extent[1], new_max_lon),
                    min(self.current_extent[2], new_min_lat),
                    max(self.current_extent[3], new_max_lat)
                ]
            if preprocessed_kalman_data is not None:
                new_min_lat = preprocessed_kalman_data['latitude'].min() - 0.5
                new_max_lat = preprocessed_kalman_data['latitude'].max() + 0.5
                new_min_lon = preprocessed_kalman_data['longitude'].min() - 0.5
                new_max_lon = preprocessed_kalman_data['longitude'].max() + 0.5
                self.current_extent = [
                    min(self.current_extent[0], new_min_lon),
                    max(self.current_extent[1], new_max_lon),
                    min(self.current_extent[2], new_min_lat),
                    max(self.current_extent[3], new_max_lat)
                ]

        self.ax.set_extent(self.current_extent, crs=ccrs.PlateCarree())
        self.ax.set_title('Trajectory on World Map')
        self.canvas.draw()

    def start_trajectory(self):
        self.data_stream_thread.start_stream()
        self.update_prediction_loop()

    def stop_trajectory(self):
        self.data_stream_thread.stop_stream()
        self.kalman_timer.stop()
        global kalman_filter_running
        kalman_filter_running = False

    def cut_data_stream(self):
        self.data_stream_thread.discard_incoming_data()
        self.update_prediction_loop(new_kalman_instance=True)

    def resume_data_stream(self):
        self.data_stream_thread.allow_incoming_data()
        global using_kalman_filter
        using_kalman_filter = False
        self.kalman_timer.stop()

    def update_prediction_loop(self, new_kalman_instance=False):
        global using_kalman_filter, kalman_filter_data, last_data_time, kalman_filter_running, predicted_data_point
        if new_kalman_instance:
            predicted_data_point = None
            if not parsed_data_df.empty:
                last_data_point = parsed_data_df.iloc[-1]
                predicted_data_point = {
                    'latitude': last_data_point['latitude'],
                    'longitude': last_data_point['longitude'],
                    'altitude': last_data_point['altitude'],
                    'timestamp': last_data_point['timestamp']
                }
                kalman_filter_data = pd.concat([kalman_filter_data, pd.DataFrame([predicted_data_point])], ignore_index=True)
        kalman_filter_running = True
        self.kalman_timer.start(1000)

    @Slot()
    def update_kalman_filter(self):
        global using_kalman_filter, kalman_filter_data, last_data_time, kalman_filter_running, predicted_data_point
        if self.data_stream_thread.discard_data and kalman_filter_running:
            using_kalman_filter = True
            for coord in ['latitude', 'longitude']:
                kalman_filters[coord].predict()
            predicted_data_point = {
                'latitude': kalman_filters['latitude'].x[0, 0], 
                'longitude': kalman_filters['longitude'].x[0, 0], 
                'altitude': kalman_filters['latitude'].x[1, 0],  # Example: using latitude's velocity as altitude
                'timestamp': pd.Timestamp.now()
            }
            kalman_filter_data = pd.concat([kalman_filter_data, pd.DataFrame([predicted_data_point])], ignore_index=True)
            self.plot_trajectory()
            last_data_time = time.time()

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
