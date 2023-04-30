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

FILENAME = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S") + '_distance_data.csv'
last_distance = None

# Open the CSV file for writing
with open(FILENAME, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['distance'])

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

        # Calculate the distance in centimeters
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        # Filter out invalid measurements
        if distance <= 50:
            # Discard readings that are more than 5 cm away from the last valid reading
            if last_distance is None or abs(distance - last_distance) <= 5:
                # Write the distance measurement to the CSV file
                writer.writerow([distance])

                # Print the distance measurement to the console
                print(f'Distance: {distance} cm')

                # Update the last valid distance
                last_distance = distance
        else:
            pass

        time.sleep(0.002)
