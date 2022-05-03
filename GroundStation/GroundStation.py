# import pygame module in this program
from time import time

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

for i in range(pygame.joystick.get_count()):
    if str(pygame.joystick.Joystick(i).get_guid()) == const.JOYSTICK_UUID:
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        break
else:
    quit()

control = Control()
telemetry = TelemetryController.Telemetry(joystick)

class GroundStation:
    def __init__(self):

        self.nc = NetworkServer()
        network_thread = tr.Thread(target=self.nc.start, daemon=True)
        network_thread.start()

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
            time1 = time()

            turn_changed = control.turn(state[pygame.K_a], state[pygame.K_d])
            if turn_changed:
                self.nc.control_steering(control.angle)

            speed_changed = control.accelerate(state[pygame.K_w], state[pygame.K_s])
            if speed_changed:
                self.nc.control_acceleration(control.speed, time1)

            if self.vc.frame is not None:
                self.display_surface.blit(self.vc.get_current_frame(), (0, 0))
            # Draws the surface object to the screen.

            telemetry.update(self.display_surface)

            pygame.display.update()


if __name__ == '__main__':
    gs = GroundStation()
