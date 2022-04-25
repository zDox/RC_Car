import os
import pickle
import socket
import sys
import threading as tr
from Network import PacketTypes as pt
from Network import NetworkConstants as const


class NetworkServer:
    def __init__(self):
        addr = socket.gethostbyname(socket.gethostname())
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((addr, const.PORT))
        self.clients = []

    def start(self):
        self.s.listen()
        print(f"\33[36;1m[LISTENING]\33[0m Server is listening.")

        while True:
            conn, addr = self.s.accept()
            thread = tr.Thread(target=self.hande_packet, args=(conn, addr), daemon=True)
            thread.start()
            self.clients.append(conn)

    def hande_packet(self, conn, addr):
        print(f"\33[36;1m[NEW CONNECTION]\33[0m {addr} connected.")
        connected = True
        while connected:
            # receive and decode the length of the message
            buffer_length = conn.recv(const.HEADER).decode(const.FORMAT)
            if not buffer_length:
                print(f"\33[33;1m[ERROR]\33[0m Lost connection with client ({addr})")
                self.clients.remove(conn)
                sys.exit()

            if buffer_length:
                action_dc = conn.recv(int(buffer_length))
                action = pickle.loads(action_dc)

    def sendAction(self, client, action, data=None):
        action_enc = pickle.dumps(action)
        buffer_length = len(action_enc)

        buffer_enc_length = str(buffer_length).encode(const.FORMAT)
        buffer_enc_length += b' ' * (
                    const.HEADER - len(buffer_enc_length))  # fill up buffer, until it has the expected size

        client.send(buffer_enc_length)
        client.send(action_enc)
        if hasattr(action, "data_length"):
            client.sendall(data)

    def control_steering(self, angle):
        action = pt.Steering(angle=angle)
        for client in self.clients:
            self.sendAction(client, action)

    def control_acceleration(self, speed):
        action = pt.Acceleration(speed=speed)
        for client in self.clients:
            self.sendAction(client, action)
