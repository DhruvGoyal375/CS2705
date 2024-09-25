import socket
import time
import random


class TimeClient:
    def __init__(self, host: str, port: int, client_id: int):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.time = time.time() + random.uniform(-5, 5)  # Simulate clock drift

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                print(f"Client {self.client_id} connected to server at {
                      self.host}:{self.port}")

                while True:
                    print(f"Client {self.client_id} current time: {
                          self.time:.2f}")
                    s.sendall(str(self.time).encode())

                    data = s.recv(1024)
                    if not data:
                        break

                    offset = float(data.decode())
                    self.time += offset
                    print(f"Client {self.client_id} received offset: {
                          offset:.2f}")
                    print(f"Client {self.client_id} adjusted time: {
                          self.time:.2f}")

                    # Wait for 5 seconds before next synchronization
                    time.sleep(5)
            except ConnectionRefusedError:
                print(
                    f"Client {self.client_id} could not connect to the server. Is it running?"
                )
            except Exception as e:
                print(f"Client {self.client_id} encountered an error: {e}")


def run_client(host, port, client_id):
    client = TimeClient(host, port, client_id)
    client.start()


if __name__ == "__main__":
    # This allows the script to be run individually for testing
    run_client("localhost", 65432, 0)
