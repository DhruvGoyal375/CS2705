import socket
import datetime
import threading

# Function to handle client requests


def handle_client(connection, address):
    print('Server connected to', address)

    # Respond to the client with the server clock time
    connection.send(str(datetime.datetime.now()).encode())

    # Close the connection with the client
    connection.close()


def initiateClockServer():
    s = socket.socket()
    print("Socket successfully created")

    # Server port
    port = 8000

    s.bind(('', port))

    # Start listening for client requests
    s.listen(5)
    print("Socket is listening...")

    # Clock Server Running forever
    while True:
        # Establish connection with client
        connection, address = s.accept()

        # Spawn a new thread to handle the client request
        client_thread = threading.Thread(
            target=handle_client, args=(connection, address))

        # Start the new thread
        client_thread.start()

        # Optionally, print how many threads are active
        print(f"Active threads: {threading.active_count()}")


# Driver function
if __name__ == '__main__':

    # Trigger the Clock Server
    initiateClockServer()
