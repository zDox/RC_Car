import Car.constants as car_const
import constants as const


class Control:
    def __init__(self):
        self.angle = 0
        self.speed = 1500



    def turn(self, left, right):
        before = self.angle
        if (left and right) or (not left and not right):
            if self.angle < 0:
                self.angle += const.STEERING_SPEED
            elif self.angle > 0:
                self.angle -= const.STEERING_SPEED
        elif left:
            if self.angle + const.STEERING_SPEED < car_const.SERVO_MAX_ANGLE:
                self.angle += const.STEERING_SPEED
        elif right:
            if self.angle - const.STEERING_SPEED > -car_const.SERVO_MAX_ANGLE:
                self.angle -= const.STEERING_SPEED
        return before != self.angle

    def wheel_turn(self, value):
        before = self.angle
        self.angle = round(value * car_const.SERVO_MAX_ANGLE)
        return before != self.angle

    def accelerate(self, accelerator, brake):
        before = self.speed
        if brake:
            if self.speed - const.BRAKE_FORCE > car_const.ESC_MIN_VALUE:
                self.speed -= const.BRAKE_FORCE
        elif accelerator:
            if self.speed + const.ACCELERATION_FORCE < car_const.ESC_MAX_VALUE:
                self.speed += const.ACCELERATION_FORCE
        return before != self.speed

    def wheel_accelerate(self, accelerator, brake):
        before = self.speed
        accelerator = (accelerator * -1 + 1) / 2
        brake = brake * -1 + 1
        if brake > const.BRAKE_PADDLE_MINIMUM_ACTIVATION:
            self.speed = car_const.ESC_DEFAULT_VALUE
        elif True:
            factor = car_const.ESC_MAX_VALUE - car_const.ESC_DEFAULT_VALUE
            self.speed = round(car_const.ESC_DEFAULT_VALUE + accelerator * factor)
        return before != self.speed
