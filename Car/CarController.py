import ServoController
import MotorController
from Network import PacketTypes as pt
from Car import NetworkController


class Car:
    def __init__(self):
        self.svc = ServoController.Servo()
        self.mtc = MotorController.Motor()
        self.nc = NetworkController.Network()
        self.nc.connect_to_server()

    def receive_controls(self):
        while True:
            control = self.nc.handle_answer()
            if isinstance(control, pt.Acceleration):
                self.mtc.set_speed(control.speed)
            if isinstance(control, pt.Steering):
                self.svc.set_angle(control.angle)


if __name__ == '__main__':
    car = Car()
    car.receive_controls()
