import RPi.GPIO as GPIO
import time
import csv
import datetime

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

FILENAME = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S_%f") + '_distance_data.csv'
last_distance = None

# Open the CSV file for writing
with open(FILENAME, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['time(ms)', 'distance(mm)'])

    while True:
        # Trigger the ultrasonic sensor to send out a pulse
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        # Measure the time it takes for the pulse to bounce back
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        # Calculate the distance in millimeters
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171500
        distance = round(distance, 2)

        # Write the distance measurement to the CSV file with current time in milliseconds
        current_time = round(time.time() * 1000)
        writer.writerow([current_time, distance])

        # Print the distance measurement to the console
        print(f'Time: {current_time} ms, Distance: {distance} mm')

        # Update the last valid distance
        last_distance = distance

        time.sleep(0.002)
