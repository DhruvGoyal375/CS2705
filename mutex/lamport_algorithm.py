import threading
import time
import random
import queue


class Process:
    def __init__(self, process_id, num_processes, message_queues):
        self.process_id = process_id
        self.num_processes = num_processes
        self.clock = 0
        self.queue = []
        self.replies = 0
        self.lock = threading.Lock()
        self.message_queues = message_queues
        self.in_critical_section = False

    def send_message(self, to_process, message_type, timestamp=None):
        self.clock += 1
        if timestamp is None:
            timestamp = self.clock
        message = (message_type, self.process_id, timestamp)
        self.message_queues[to_process].put(message)
        print(f"Process {self.process_id} sent {message_type} message to Process {
              to_process} with timestamp {timestamp}")

    def receive_message(self):
        message = self.message_queues[self.process_id].get()
        message_type, sender_id, timestamp = message
        self.clock = max(self.clock, timestamp) + 1
        print(f"Process {self.process_id} received {
              message_type} message from Process {sender_id} with timestamp {timestamp}")
        return message

    def request_critical_section(self):
        with self.lock:
            self.clock += 1
            request_timestamp = self.clock
            self.queue.append((request_timestamp, self.process_id))
            self.queue.sort()

        for i in range(self.num_processes):
            if i != self.process_id:
                self.send_message(i, "REQUEST", request_timestamp)

        self.replies = 0
        while self.replies < self.num_processes - 1 or self.queue[0] != (
            request_timestamp,
            self.process_id,
        ):
            self.process_messages()

    def release_critical_section(self):
        with self.lock:
            self.queue.pop(0)

        for i in range(self.num_processes):
            if i != self.process_id:
                self.send_message(i, "RELEASE")

    def handle_request(self, sender_id, timestamp):
        with self.lock:
            self.queue.append((timestamp, sender_id))
            self.queue.sort()
            self.send_message(sender_id, "REPLY", timestamp)

    def handle_reply(self, sender_id, timestamp):
        self.replies += 1

    def handle_release(self, sender_id, timestamp):
        with self.lock:
            self.queue = [(t, p) for t, p in self.queue if p != sender_id]

    def process_messages(self):
        while not self.message_queues[self.process_id].empty():
            message_type, sender_id, timestamp = self.receive_message()
            if message_type == "REQUEST":
                self.handle_request(sender_id, timestamp)
            elif message_type == "REPLY":
                self.handle_reply(sender_id, timestamp)
            elif message_type == "RELEASE":
                self.handle_release(sender_id, timestamp)


def process_thread(process):
    for _ in range(
        3
    ):  # Each process will attempt to enter the critical section 3 times
        # Simulate some work
        # time.sleep(random.uniform(0.5, 2))

        # Request critical section
        process.request_critical_section()

        # Enter critical section
        process.in_critical_section = True
        print(f"Process {process.process_id} entered critical section")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"Process {process.process_id} exited critical section")
        process.in_critical_section = False

        # Release critical section
        process.release_critical_section()


def main():
    num_processes = 3
    message_queues = [queue.Queue() for _ in range(num_processes)]
    processes = [
        Process(i, num_processes, message_queues) for i in range(num_processes)
    ]

    threads = []
    for process in processes:
        thread = threading.Thread(target=process_thread, args=(process,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
