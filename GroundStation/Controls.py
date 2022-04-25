import Car.constants as car_const
import constants as const


class Control:
    def __init__(self):
        self.angle = 0
        self.speed = 1500

    def turn(self, left, right):
        if (left and right) or (not left and not right):
            if self.angle < 0:
                self.angle += const.STEERING_SPEED
            elif self.angle > 0:
                self.angle -= const.STEERING_SPEED
        elif left:
            if self.angle - const.STEERING_SPEED > -car_const.SERVO_MAX_ANGLE:
                self.angle -= const.STEERING_SPEED
        elif right:
            if self.angle + const.STEERING_SPEED < car_const.SERVO_MAX_ANGLE:
                self.angle += const.STEERING_SPEED

    def accelerate(self, accelerator, brake):
        if brake:
            if self.speed - const.BRAKE_FORCE > car_const.ESC_MIN_VALUE:
                self.speed -= const.BRAKE_FORCE
        elif accelerator:
            if self.speed + const.ACCELERATION_FORCE < car_const.ESC_MAX_VALUE:
                self.speed += const.ACCELERATION_FORCE
