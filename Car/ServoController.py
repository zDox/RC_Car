from gpiozero import AngularServo
from time import sleep
import constants as const


class Servo:
    def __init__(self):
        self.servo = AngularServo(const.SERVO_PIN, min_pulse_width=const.SERVO_MIN_PULSE_WIDTH,
                                  max_pulse_width=const.SERVO_MAX_PULSE_WIDTH)
        self.servo.angle = 0

    def set_angle(self, angle):
        angle = float(angle)
        if -const.SERVO_MAX_ANGLE <= angle <= const.SERVO_MAX_ANGLE:
            self.servo.angle = angle
