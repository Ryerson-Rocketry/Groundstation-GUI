import pandas as pd
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pynmea2

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
    msg = pynmea2.parse(nmea_str)
    return {
        'latitude': msg.latitude,
        'longitude': msg.longitude,
        'altitude': msg.altitude,
        'timestamp': msg.timestamp
    }

#can do +/- 2 

nmea_str = "$GPGGA,123456.00,4916.45,N,12311.12,W,1,08,0.9,545.4,M,46.9,M,,*47"

nmea_dataset = [
"$GPGGA,000000.00,3452.01,N,11814.04,W,1,08,0.9,100.0,M,0.0,M,,*47",
"$GPGGA,000001.00,3452.02,N,11814.05,W,1,08,0.9,150.0,M,0.0,M,,*47",
"$GPGGA,000002.00,3452.03,N,11814.06,W,1,08,0.9,200.0,M,0.0,M,,*47",
"$GPGGA,000003.00,3452.04,N,11814.07,W,1,08,0.9,250.0,M,0.0,M,,*47",
"$GPGGA,000004.00,3452.05,N,11814.08,W,1,08,0.9,300.0,M,0.0,M,,*47",
"$GPGGA,000005.00,3452.06,N,11814.09,W,1,08,0.9,350.0,M,0.0,M,,*47",
"$GPGGA,000006.00,3452.07,N,11814.10,W,1,08,0.9,400.0,M,0.0,M,,*47",
"$GPGGA,000007.00,3452.08,N,11814.11,W,1,08,0.9,450.0,M,0.0,M,,*47",
"$GPGGA,000008.00,3452.09,N,11814.12,W,1,08,0.9,500.0,M,0.0,M,,*47",
"$GPGGA,000009.00,3452.10,N,11814.13,W,1,08,0.9,550.0,M,0.0,M,,*47",
"$GPGGA,000010.00,3452.11,N,11814.14,W,1,08,0.9,600.0,M,0.0,M,,*47"
]

nmeas = ["$GPGSV,2,1,08,02,74,042,45,04,18,190,36,07,67,279,42,12,29,323,36*77",
            "$GPGSV,2,2,08,15,30,050,47,19,09,158,,26,12,281,40,27,38,173,41*7B"]

for msg in nmeas:
    print(calculate_checksum(msg))

parsed_data_list = [parse_nmea_message(nmea_str) for nmea_str in nmeas]

# Filter out any None values in case of parsing errors
parsed_data_list = [data for data in parsed_data_list if data is not None]

# Convert the list of dictionaries to a DataFrame
parsed_data_df = pd.DataFrame(parsed_data_list)

def pre_process(data):
    data = data.dropna()
    data['x'] = data['latitude'] * 111000
    data['y'] = data['longitude'] * 111000
    return data

# Preprocess the DataFrame
preprocessed_data = pre_process(parsed_data_df)
print(preprocessed_data)




def predict_trajectory(self, data, steps):
    kf = self.initializa_kalman_filter()
    trajectory = []

    for i in range(len(data)):
        kf.predict(u=0)
        kf.update(data[i])
        trajectory.append(kf.x.flatten())

    for _ in range(steps):
        kf.predict(u=0)
        trajectory.append(kf.x.flatten())

    return np.array(trajectory)


def plot_trajectory(self, data):
    self.ax.clear()
    self.ax.plot(data['x'], data['y'], label="Actual Trajectory")

    predict_trajectory = self.predict_trajectory(data[['x', 'y']].values, steps=10)
    self.ax.plot(predict_trajectory[:, 0], predict_trajectory[:, 1], label="Predicted Trajectory")

    self.ax.legend()

    self.canvas.draw()