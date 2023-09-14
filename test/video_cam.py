# import required libraries

from vidgear.gears import CamGear, NetGear
import cv2
from time import sleep, monotonic


class Cam:
    def __init__(self):
        # Open suitable video stream, such as webcam on first index(i.e. 0)
        cam_options = {
            "CAP_PROP_FRAME_WIDTH": 1920,  # resolution 320x240
            "CAP_PROP_FRAME_HEIGHT": 1080,
            "CAP_PROP_FPS": 30,  # framerate 60fps
            "CAP_PROP_CONVERT_RGB": 1,
            "CAP_PROP_FOURCC": cv2.VideoWriter.fourcc("M", "J", "P", "G"),
        }
        self.stream = CamGear(source=2, **cam_options).start()
        # define tweak flags
        options = {"flag": 0,
                   "copy": False,
                   "track": False,
                   "jpeg_compression": True,
                   "jpeg_compression_quality": 70,
                   "jpeg_compression_fastdct": True,
                   "jpeg_compression_fastupsample": True,
                   }


cam = Cam()
t1 = monotonic()
for _ in range(90):
    frame = cam.stream.read()
    sleep(0.05)
print(monotonic() - t1)
