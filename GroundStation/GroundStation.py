# import pygame module in this program
from time import sleep

import pygame
import threading as tr

import constants as const
import TelemetryController
from Controls import Control
import VideoController
from NetworkServer import NetworkServer
from colors import *

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

telemetry = TelemetryController.Telemetry(joystick)
font = pygame.font.Font(None, 20)


class GroundStation:
    def __init__(self):
        self.c = Control()
        self.nc = NetworkServer()
        network_thread = tr.Thread(target=self.nc.start, daemon=True)
        network_thread.start()

        control_thread = tr.Thread(target=self.update_controls, daemon=True)
        control_thread.start()

        self.vc = VideoController.Video()
        video_thread = tr.Thread(target=self.vc.receive_data, daemon=True)
        video_thread.start()

        self.display_surface = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption('RC Car Control')

        self.clock = pygame.time.Clock()
        self.update()

    def update(self):
        # infinite loop

        while True:
            self.clock.tick(const.FPS)
            self.display_surface.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            state = pygame.key.get_pressed()

            if self.vc.frame is not None:
                self.display_surface.blit(self.vc.get_current_frame(), (0, 0))
            # Draws the surface object to the screen.
            speed = font.render(f"{self.c.angle}", True, BLACK)

            self.display_surface.blit(speed, (300, 200))

            telemetry.update(self.display_surface)

            pygame.display.update()

    def update_controls(self):
        while True:
            turn_changed = self.c.wheel_turn(joystick.get_axis(const.WHEEL_AXIS))
            if turn_changed:
                self.nc.control_steering(self.c.angle * -1)

            speed_changed = self.c.wheel_accelerate(joystick.get_axis(const.THROTTLE_PEDAL_AXIS),
                                                    joystick.get_axis(const.BRAKE_PEDAL_AXIS))
            if speed_changed:
                self.nc.control_acceleration(self.c.speed)
            sleep(0.1)


if __name__ == '__main__':
    gs = GroundStation()
