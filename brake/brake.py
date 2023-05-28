import csv
import smbus
import math
import time

# MPU6050 registers and constants
DEVICE_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Define the mass of the bike and rider
mass = 80  # kg

# Define the gravitational acceleration
g = 9.81  # m/s^2

# Get I2C bus
bus = smbus.SMBus(1)

# Read data from MPU6050
def read_data(address):
    high = bus.read_byte_data(DEVICE_ADDRESS, address)
    low = bus.read_byte_data(DEVICE_ADDRESS, address+1)
    value = (high << 8) + low
    if value > 32768:
        value = value - 65536
    return value

# Initialize MPU6050
bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)
bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)
bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)
bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 24)
bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)

# Open CSV file for writing
with open('output.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(['Time', 'Pressure Applied (N)'])

    # Read and print data from MPU6050
    while True:
        # Get current time
        current_time = time.time()

        # Read accelerometer data
        gyro_y = read_data(GYRO_YOUT_H)

        # Convert raw data to degrees per second and gravity acceleration
        gyro_y = gyro_y / 131.0
        pressure = mass * (gyro_y - g)

        # Print and write data
        print('Pressure Applied (N):  Y=%.2f' % pressure)
        csvwriter.writerow([current_time, pressure])

        # Wait for some time before reading again
        time.sleep(1)
