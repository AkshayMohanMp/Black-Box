import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
TRIG1 = 8
ECHO1 = 10
TRIG2 = 16
ECHO2 = 18
GPIO.setwarnings(False)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

# Create a new CSV file for each session
file_path = "/home/cev/Desktop/New"
filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Distance 1 (cm)", "Distance 2 (cm)", "Status", "Timestamp"])

    while True:
        # Sensor 1
        GPIO.output(TRIG1, False)
        time.sleep(2)

        GPIO.output(TRIG1, True)
        time.sleep(0.00001)
        GPIO.output(TRIG1, False)

        while GPIO.input(ECHO1)==0:
            pulse_start1 = time.time()

        while GPIO.input(ECHO1)==1:
            pulse_end1 = time.time()

        pulse_duration1 = pulse_end1 - pulse_start1
        distance1 = pulse_duration1 * 17150
        distance1 = round(distance1, 2)

        # Sensor 2
        GPIO.output(TRIG2, False)
        time.sleep(2)

        GPIO.output(TRIG2, True)
        time.sleep(0.00001)
        GPIO.output(TRIG2, False)

        while GPIO.input(ECHO2)==0:
            pulse_start2 = time.time()

        while GPIO.input(ECHO2)==1:
            pulse_end2 = time.time()

        pulse_duration2 = pulse_end2 - pulse_start2
        distance2 = pulse_duration2 * 17150
        distance2 = round(distance2, 2)

        # Compare distances and write to CSV
        if distance1 > 0 and distance1 < 400 and distance2 > 0 and distance2 < 400:
            status = "Good" if distance1 > 100 and distance2 > 100 else "Bad"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [distance1, distance2, status, timestamp]
            print("Distance 1:", distance1, "cm")
            print("Distance 2:", distance2, "cm")
            print("Status:", status)
            writer.writerow(data)
            time.sleep(0.5)
        else:
            print("Out of range")
