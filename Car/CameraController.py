# import required libraries
import asyncio

from vidgear.gears import CamGear
from vidgear.gears.asyncio import NetGear_Async
import cv2

from Network import NetworkConstants as const


class Cam:
    def __init__(self):
        # Open suitable video stream, such as webcam on first index(i.e. 0)
        cam_options = {
            "CAP_PROP_FRAME_WIDTH": 640,  # resolution 320x240
            "CAP_PROP_FRAME_HEIGHT": 360,
            "CAP_PROP_FPS": 30,  # framerate 60fps
        }
        self.stream = CamGear(source=0, **cam_options).start()
        # define tweak flags
        options = {"flag": 0,
                   "copy": False,
                   "track": False,
                   "jpeg_compression": True,
                   "jpeg_compression_quality": 70,
                   "jpeg_compression_fastdct": True,
                   "jpeg_compression_fastupsample": True,
                   }
        self.server = NetGear_Async(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            protocol="tcp",
            logging=False,
            **options
        )

    def cam(self):
        asyncio.set_event_loop(self.server.loop)
        # Add your custom source generator to Server configuration
        self.server.config["generator"] = self.my_frame_generator()
        # Launch the Server
        self.server.launch()
        try:
            self.server.loop.run_until_complete(self.server.task)
        except SystemExit:
            pass
        finally:
            self.stream.release()
            self.server.close()

    async def my_frame_generator(self):
        while True:
            frame = self.stream.read()
            yield frame
            await asyncio.sleep(0)
