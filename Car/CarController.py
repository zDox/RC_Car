import os
import sys

import constants as const

import ServoController
import MotorController

current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from Network import PacketTypes as pt
from Car import NetworkController


class CarControllerClass():
    def __init__(self):
        self.svc = ServoController.Servo()
        self.mtc = MotorController.Motor()
        self.nc = NetworkController.Network()
        self.nc.connect_to_server()

    def __enter__(self):
        print("Controller started")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.svc.set_angle(0)
        self.mtc.set_speed(const.ESC_DEFAULT_VALUE)

    def receive_controls(self):
        while True:
            control = self.nc.handle_answer()
            if isinstance(control, pt.Acceleration):
                self.mtc.set_speed(control.speed)
            if isinstance(control, pt.Steering):
                self.svc.set_angle(control.angle)


if __name__ == '__main__':
    with CarControllerClass() as car:
        car.receive_controls()
