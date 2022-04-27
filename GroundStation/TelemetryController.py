import pygame
import constants as const
from colors import *


class Telemetry:
    def __init__(self, joystick: pygame.joystick.Joystick):
        self.joystick = joystick
        self.x = const.SCREEN_WIDTH // 1.5
        self.y = const.SCREEN_HEIGHT // 2
        self.bars = []
        pointer = self.x
        # Create Bars for Axis listed in constants.py
        for bar in const.BARS:
            self.bars.append(Bar(bar[0], pointer, bar[2], bar[1]))
            pointer += const.BAR_OFFSET + const.BAR_WIDTH
        pointer += const.WHEEL_OFFSET
        # Create Steering Wheel
        self.wheel = Wheel(pointer, const.SCREEN_HEIGHT - const.DEFAULT_IMAGE_SIZE[1])
        pointer += self.wheel.image.get_size()[0]

    def update(self, screen):
        for bar in self.bars:
            value = (self.joystick.get_axis(bar.axis) * -1 + 1) / 2 * const.SCREEN_HEIGHT / 10
            bar.update(screen, value)
        wheel_value = (self.joystick.get_axis(0) * -1)
        self.wheel.update(screen, wheel_value)


class Bar:
    def __init__(self, axis, x, color, description):
        self.axis = axis
        self.x = x
        self.color = color
        self.description = description

    def update(self, screen, value):
        rect = [self.x, const.SCREEN_HEIGHT - value, const.BAR_WIDTH, value]
        pygame.draw.rect(screen, self.color, rect)


class Wheel:
    def __init__(self, x, y):
        self.axis = 0
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("Assets/wheel.png"), const.DEFAULT_IMAGE_SIZE)

    def update(self, screen, value):
        rotated_image = pygame.transform.rotate(self.image, value * 450)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)

        screen.blit(rotated_image, new_rect)
