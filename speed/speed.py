import csv
import time
import math
from MPU6050 import MPU6050  # Assuming you have the MPU6050 library installed

# Initialize the MPU-6050 sensor
sensor = MPU6050()

# Set the sensor sensitivity (adjust if needed)
sensor.set_accel_range(sensor.ACCEL_RANGE_2G)

# Constants for speed calculation
SAMPLE_INTERVAL = 0.1  # Time interval between speed calculations (in seconds)
GRAVITY = 9.81  # Acceleration due to gravity (in m/s^2)

# Variables for speed calculation
prev_velocity = 0.0
prev_time = time.time()

# Open the CSV file in write mode
with open('speed_classification.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Speed (km/h)', 'Classification'])  # Write header row
    
    # Main loop
    while True:
        # Read accelerometer data
        acceleration = sensor.get_accel_data()
        accel_x = acceleration['x']
        accel_y = acceleration['y']
        accel_z = acceleration['z']
        
        # Calculate the total acceleration (excluding gravity)
        total_accel = math.sqrt(accel_x**2 + accel_y**2 + (accel_z-GRAVITY)**2)
        
        # Calculate the elapsed time since the last speed calculation
        current_time = time.time()
        elapsed_time = current_time - prev_time
        
        # Calculate the current velocity using the average acceleration over the elapsed time
        current_velocity = prev_velocity + (total_accel * elapsed_time)
        
        # Update variables for the next iteration
        prev_velocity = current_velocity
        prev_time = current_time
        
        # Convert velocity from m/s to km/h
        speed = current_velocity * 3.6
        
        # Classify the driver based on the speed
        if speed > 70:
            classification = "Rash Driving Detected!"
        else:
            classification = "Normal Driving"
        
        # Print the current speed and classification
        print("Current Speed: {:.2f} km/h".format(speed))
        print(classification)
        
        # Write the speed and classification to the CSV file
        writer.writerow([speed, classification])
        
        # Wait for the next speed calculation
        time.sleep(SAMPLE_INTERVAL)
