# import required libraries
from vidgear.gears import NetGear
import cv2

from Network import NetworkConstants as const


class Cam:
    def __init__(self):
        # Open suitable video stream, such as webcam on first index(i.e. 0)
        self.stream = cv2.VideoCapture(0)
        self.stream.set(3, 1920)
        self.stream.set(4, 1080)
        self.stream.set(6, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
        # define tweak flags
        options = {"flag": 0, "copy": False, "track": False}
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
            (grabbed, frame) = self.stream.read()
            # check for frame if not grabbed
            if not grabbed:
                break
            # send frame to server
            self.server.send(frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.release()
        self.server.close()
