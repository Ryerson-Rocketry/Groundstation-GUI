import pandas as pd
import numpy as np
import pynmea2
import time
import random
import threading
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class Trajectory:
    def __init__(self):
        self.parsed_data_df = pd.DataFrame(columns=['latitude', 'longitude', 'altitude', 'timestamp'])
        self.start_stream_thread()

    def calculate_checksum(self, nmea_str):
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

    def parse_nmea_message(self, nmea_str):
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

    def pre_process(self, data):
        data = data.dropna()
        return data

    def decimal_to_dm(self, dec):
        degrees = int(dec)
        minutes = (dec - degrees) * 60
        return f"{degrees * 100 + minutes:.4f}"

    def generate_nmea_message(self):
        lat = 34.5201 + random.uniform(-0.001, 0.001)
        lon = -118.1404 + random.uniform(-0.001, 0.001)
        alt = random.uniform(100.0, 600.0)
        timestamp = pd.Timestamp.now().strftime("%H%M%S.00")
        lat_dm = self.decimal_to_dm(lat)
        lon_dm = self.decimal_to_dm(-lon)  # Convert to positive for NMEA format
        nmea_message = f"GPGGA,{timestamp},{lat_dm},N,{lon_dm},W,1,08,0.9,{alt:.1f},M,0.0,M,,"
        checksum = 0
        for char in nmea_message:
            checksum ^= ord(char)
        checksum_str = f"*{checksum:02X}"
        complete_message = f"${nmea_message}{checksum_str}"
        return complete_message

    def process_stream(self):
        while True:
            nmea_message = self.generate_nmea_message()
            parsed_data = self.parse_nmea_message(nmea_message)
            if parsed_data:
                new_data_df = pd.DataFrame([parsed_data])
                self.parsed_data_df = pd.concat([self.parsed_data_df, new_data_df], ignore_index=True)
            time.sleep(1)  # Simulate a delay between incoming messages

    def start_stream_thread(self):
        stream_thread = threading.Thread(target=self.process_stream)
        stream_thread.daemon = True
        stream_thread.start()
