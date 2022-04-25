import socket
import pickle
from time import sleep

from Network import PacketTypes as pt
from Network import NetworkConstants as const


class Network:
    def __init__(self):
        self.addr = const.SERVER_IP, const.PORT  # address for socket to connect to

        self.client = socket.socket()
        self.connected = False

    def connect_to_server(self):
        while not self.connected:
            try:
                self.client = socket.socket()
                self.client.connect(self.addr)
                self.connected = True
                break
            except socket.error:
                sleep(0.5)

    def sendAction(self, action, data=None):
        action_enc = pickle.dumps(action)
        buffer_length = len(action_enc)

        buffer_enc_length = str(buffer_length).encode(const.FORMAT)
        buffer_enc_length += b' ' * (const.HEADER - len(buffer_enc_length))  # fill up buffer, until it has the expected size

        self.client.send(buffer_enc_length)
        self.client.send(action_enc)
        if hasattr(action, "data_length"):
            self.client.sendall(data)

    def handle_answer(self):
        # receive and decode the length of the message
        buffer_length = self.client.recv(const.HEADER).decode(const.FORMAT)
        if not buffer_length:
            self.connected = False
            quit()
            self.connect_to_server()
            self.handle_answer()
        if buffer_length:
            action_dc = self.client.recv(int(buffer_length))
            action = pickle.loads(action_dc)
            if isinstance(action, pt.Steering) or isinstance(action, pt.Acceleration):
                return action
