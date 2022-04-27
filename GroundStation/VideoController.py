from vidgear.gears import NetGear
import cv2

from Network import NetworkConstants as const


class Video:
    def __init__(self):
        options = {"flag": 0, "copy": False, "track": False}
        self.client = NetGear(
            address=const.SERVER_IP,
            port=const.VIDEO_PORT,
            protocol="tcp",
            pattern=0,
            receive_mode=True,
            logging=False,
            **options
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

        # safely close client
        self.client.close()

        # loop over

    def receiv_data(self):
        while True:

            # receive frames from network
            frame = self.client.recv()

            # check for received frame if Nonetype
            if frame is None:
                break

            # {do something with the received frame here}

            # Show output window
            cv2.imshow("Output Frame", frame)

            # check for 'q' key if pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
