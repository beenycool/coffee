# networking.py
# Handles multiplayer networking for FPS game

import socket
import threading

class NetworkClient:
    def __init__(self, server_ip, server_port, on_data):
        self.server_addr = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.on_data = on_data
        self.running = True
        threading.Thread(target=self.network_thread, daemon=True).start()

    def send(self, msg):
        self.sock.sendto(msg.encode(), self.server_addr)

    def network_thread(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                self.on_data(data.decode())
            except BlockingIOError:
                pass

    def close(self):
        self.running = False
        self.sock.close()