import serial
import pynmea2
import csv
from datetime import datetime

# Open a serial connection to the GPS module
ser = serial.Serial(port='/dev/serial0', baudrate=9600)

# Create a new CSV file for each session
#| 8 | GPIO 14 (TXD) | 14 | UART0 TXD | Serial Transmit |
#| 10 | GPIO 15 (RXD) | 15 | UART0 RXD | Serial Receive |
with open('turn_speed.csv', mode='w') as csv_file:
    file_path = "/home/cev/Desktop/New"
    fieldnames = ['Latitude', 'Longitude', 'Timestamp']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Set the GPS status variable
    gps_enabled = 1

    # Read GPS data continuously
    while True:
        # Read a line of GPS data from the serial connection
        data = ser.readline().decode('ascii')

        # Check if the data is a valid NMEA sentence
        if data.startswith('$GPGGA'):
            # Parse the NMEA sentence
            msg = pynmea2.parse(data)

            # Check if the GPS status is "BAD"
            if msg.gps_qual == 0:
                # Print the coordinates and write the data to the CSV file
                if gps_enabled == 1:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data = [msg.latitude, msg.longitude, timestamp]
                    print("Latitude:", msg.latitude)
                    print("Longitude:", msg.longitude)
                    writer.writerow(data)
