import socket
import threading
import time
from typing import List, Tuple


class TimeServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.time = time.time()
        self.clients: List[Tuple[socket.socket, float]] = []

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print(f"Connected by {addr}")
                client_thread = threading.Thread(
                    target=self.handle_client, args=(conn,)
                )
                client_thread.start()

    def handle_client(self, conn: socket.socket):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                client_time = float(data.decode())
                time_diff = client_time - self.time
                self.clients.append((conn, time_diff))

                if len(self.clients) >= 3:
                    self.synchronize()

    def synchronize(self):
        total_diff = sum(diff for _, diff in self.clients)
        average_offset = total_diff / (
            len(self.clients) + 1
        )  # +1 to include the server

        for conn, _ in self.clients:
            conn.sendall(str(average_offset).encode())

        self.time += average_offset
        print(f"Synchronized time: {self.time}")
        self.clients.clear()


if __name__ == "__main__":
    server = TimeServer("localhost", 65432)
    server.start()
