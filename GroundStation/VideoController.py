import asyncio

import pygame
from vidgear.gears.asyncio import NetGear_Async
import cv2

from Network import NetworkConstants as const
import constants as c_const


class Video:
    def __init__(self):
        self.frame = None
        options = {"flag": 0,
                   "copy": False,
                   "track": False,
                   }
        self.client = NetGear_Async(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            receive_mode=True,
            logging=False,
            **options
        ).launch()

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

        # safely close client
        self.client.close()

        # loop over

    def video(self):
        asyncio.set_event_loop(self.client.loop)
        try:
            self.client.loop.run_until_complete(self.receive_data())
        except SystemExit:
            pass

    async def receive_data(self):
        async for frame in self.client.recv_generator():

            self.frame = pygame.transform.scale(pygame.image.frombuffer(frame.tostring(), (frame.shape[1::-1]),
                                                                        "RGB"), (1776, 1000))
            await asyncio.sleep(0)

    def get_current_frame(self):
        return self.frame
