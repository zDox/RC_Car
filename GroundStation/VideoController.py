import pygame
from vidgear.gears import NetGear
import cv2

from Network import NetworkConstants as const


class Video:
    def __init__(self):
        self.frame = None
        options = {"flag": 0,
                   "copy": False,
                   "track": False,
                   }
        self.client = NetGear(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            pattern=0,
            receive_mode=True,
            logging=True,
            **options
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

        # safely close client
        self.client.close()

        # loop over

    def receive_data(self):
        while True:
            self.frame = self.client.recv()
            if self.frame.all():
                break

    def get_current_frame(self):
        return pygame.transform.scale(pygame.image.frombuffer(self.frame.tostring(), (self.frame.shape[1::-1]),
                                                                        "RGB"), (1776, 1000))
