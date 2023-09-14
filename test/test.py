import pygame
from time import sleep
pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
logitech = pygame.joystick.Joystick(0)
logitech.init()
last_values = []
while True:
    for axis_id in range(logitech.get_numaxes()):
        print(logitech.get_axis(axis_id), end="")
    print("")

