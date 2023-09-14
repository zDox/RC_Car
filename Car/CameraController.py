# import required libraries

from vidgear.gears import CamGear, NetGear
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
        self.stream = CamGear(source=0, colorspace="COLOR_BGR2RGB", **cam_options).start()
        # define tweak flags
        options = {"flag": 0,
                   "copy": False,
                   "track": False,
                   "jpeg_compression": True,
                   "jpeg_compression_quality": 70,
                   "jpeg_compression_fastdct": True,
                   "jpeg_compression_fastupsample": True,
                   }
        self.server = NetGear(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            protocol="tcp",
            pattern=0,
            logging=False,
            **options
        )

    def my_frame_generator(self):
        while True:
            frame = self.stream.read()
            if frame is None:
                break
            self.server.send(frame)
