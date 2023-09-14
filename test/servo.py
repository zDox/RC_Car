from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, <min_pulse_width=0.0006, max_pulse_width=0.0023)
while True:
     angle = int(input("Angle:" ))
     if -45 <= angle <= 45:
          servo.angle = angle