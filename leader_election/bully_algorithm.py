class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.is_coordinator = False

    def initiate_election(self, nodes):
        print(f"Node {self.node_id} initiates election.")

        higher_priority_nodes = [
            node for node in nodes if node.node_id > self.node_id]

        if not higher_priority_nodes:
            # If no higher priority node exists, current node becomes the coordinator
            self.become_coordinator()
        else:
            # Send election message to higher priority nodes
            for node in higher_priority_nodes:
                node.receive_election_message(self)

    def receive_election_message(self, sender):
        print(f"Node {self.node_id} receives election message from Node {
              sender.node_id}.")

        if self.node_id > sender.node_id:
            print(f"Node {self.node_id} responds to Node {sender.node_id}.")
            sender.receive_response(self)

            # Now this node initiates its own election process
            self.initiate_election(nodes)

    def receive_response(self, sender):
        print(f"Node {self.node_id} receives response from Node {
              sender.node_id}.")

    def become_coordinator(self):
        print(f"Node {self.node_id} becomes the coordinator.")
        self.is_coordinator = True


if __name__ == "__main__":
    # Create nodes
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)

    # List of nodes in the distributed system
    nodes = [node1, node2, node3, node4, node5]

    # Simulate failure of current coordinator (Node 3)
    node3.is_coordinator = False

    # Assume Node 3 detects coordinator failure and initiates election
    node3.initiate_election(nodes)
