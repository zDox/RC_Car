# import required libraries
from vidgear.gears import NetGear, CamGear
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
                   }
        self.server = NetGear(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            protocol="tcp",
            pattern=0,
            logging=False,
            **options
        )

    def send_data(self):
        while True:
            # read frames from stream
            frame = self.stream.read()
            # check for frame if not grabbed
            if frame is None:
                break
            # send frame to server
            self.server.send(frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.release()
        self.server.close()
