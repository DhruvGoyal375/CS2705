import threading
from berkleys_client import run_client


def launch_clients(num_clients, host, port):
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=run_client, args=(host, port, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    NUM_CLIENTS = 5
    SERVER_HOST = "localhost"
    SERVER_PORT = 65432

    launch_clients(NUM_CLIENTS, SERVER_HOST, SERVER_PORT)
