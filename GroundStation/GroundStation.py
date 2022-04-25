# import pygame module in this program
from time import time

import pygame
import threading as tr

import constants as const
from Controls import Control
from NetworkServer import NetworkServer

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

control = Control()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

X = 400
Y = 400


class GroundStation:
    def __init__(self):

        self.nc = NetworkServer()
        thread = tr.Thread(target=self.nc.start, daemon=True)
        thread.start()

        self.display_surface = pygame.display.set_mode((X, Y))
        pygame.display.set_caption('Show Text')

        self.clock = pygame.time.Clock()
        self.update()

    def update(self):
        # infinite loop
        font = pygame.font.Font(None, 32)

        while True:
            self.clock.tick(const.FPS)

            self.display_surface.fill(white)

            text = font.render(f"{control.angle}", True, green, blue)

            textRect = text.get_rect()

            textRect.center = (X // 2, Y // 2)

            self.display_surface.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    # quit the program.
                    quit()

            state = pygame.key.get_pressed()
            time1 = time()
            control.turn(state[pygame.K_a], state[pygame.K_d])
            control.accelerate(state[pygame.K_w], state[pygame.K_s])
            self.nc.control_steering(control.angle)
            self.nc.control_acceleration(control.speed, time1)

            # Draws the surface object to the screen.
            pygame.display.update()


if __name__ == '__main__':
    gs = GroundStation()
