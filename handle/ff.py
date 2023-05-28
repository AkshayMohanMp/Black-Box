import csv
import time
from mpu6050 import mpu6050

sensor1 = mpu6050(0x68)  # MPU 6050 on the right side of the bike
sensor2 = mpu6050(0x69)  # MPU 6050 on the left side of the bike

with open('turn_speed.csv', mode='w') as csv_file:
    file_path = "/home/cev/Desktop/New"
    fieldnames = ['timestamp', 'right_turn_speed', 'left_turn_speed']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        timestamp = time.time()
        gyro_data1 = sensor1.get_gyro_data()
        gyro_data2 = sensor2.get_gyro_data()

        right_turn_speed = gyro_data1['y']
        left_turn_speed = gyro_data2['y']

        writer.writerow({'timestamp': timestamp,
                         'right_turn_speed': right_turn_speed,
                         'left_turn_speed': left_turn_speed})
        print(f'Timestamp: {timestamp}, ' f'Right turn speed: {right_turn_speed}, ' f'Left turn speed: {left_turn_speed}')

        time.sleep(0.1) # sampling rate of 10 Hz
