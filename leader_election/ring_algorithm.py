class Process:
    def __init__(self, id):
        self.id = id
        self.active = True
        self.next = None

def ring_leader_election(processes):
    # Initialize the ring
    for i in range(len(processes)):
        processes[i].next = processes[(i + 1) % len(processes)]
    
    leader = None
    round = 1

    while leader is None:
        print(f"Round {round}")
        for process in processes:
            if process.active:
                # Send ID around the ring
                current = process.next
                max_id = process.id
                while current != process:
                    if current.id > max_id:
                        max_id = current.id
                    current = current.next
                
                # Compare received maximum ID with own ID
                if max_id > process.id:
                    process.active = False
                    print(f"Process {process.id} becomes inactive")
                elif max_id == process.id:
                    leader = process
                    print(f"Process {process.id} declares itself as the leader")
                    break
        round += 1
    
    return leader

# Create 6 processes
processes = [Process(i) for i in range(1, 7)]

# Run the election
elected_leader = ring_leader_election(processes)

print(f"The elected leader is Process {elected_leader.id}")