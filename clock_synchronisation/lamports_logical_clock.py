# Function to find the maximum timestamp between 2 events
def max1(a, b):
    return a if a > b else b


# Function to display the logical timestamps
def display(e1, e2, p1, p2):
    print("\nThe time stamps of events in P1:")
    for i in range(e1):
        print(f"e1{i + 1}: {p1[i]}", end=" ")

    print("\nThe time stamps of events in P2:")
    for i in range(e2):
        print(f"e2{i + 1}: {p2[i]}", end=" ")


# Function to find the timestamps of events using Lamport's Logical Clock
def lamportLogicalClock(e1, e2, m):
    p1 = [0] * e1
    p2 = [0] * e2

    # Initialize p1[] and p2[] with event numbers
    for i in range(e1):
        p1[i] = i + 1

    for i in range(e2):
        p2[i] = i + 1

    # Display initial matrix
    print("Initial event matrix (m):")
    for i in range(e1):
        print(f"e1{i+1}", end="\t")
        for j in range(e2):
            print(m[i][j], end="\t")
        print()

    # Loop through the event matrix to adjust logical clocks
    for i in range(e1):
        for j in range(e2):
            if m[i][j] == 1:  # Message is sent from P1 to P2
                p2[j] = max1(p2[j], p1[i] + 1)  # Update P2 timestamp
                # Propagate changes to subsequent events in P2
                for k in range(j + 1, e2):
                    p2[k] = p2[k - 1] + 1

            elif m[i][j] == -1:  # Message is received by P1 from P2
                p1[i] = max1(p1[i], p2[j] + 1)  # Update P1 timestamp
                # Propagate changes to subsequent events in P1
                for k in range(i + 1, e1):
                    p1[k] = p1[k - 1] + 1

    # Display final timestamps
    display(e1, e2, p1, p2)


# Driver code
if __name__ == "__main__":
    e1 = 5  # Number of events in process P1
    e2 = 3  # Number of events in process P2

    # Matrix defining the message dependencies:
    # 1 = message sent, -1 = message received, 0 = no message
    m = [[0] * e2 for _ in range(e1)]

    m[0][0] = 0  # No message sent or received at e1, e2
    m[0][1] = 0
    m[0][2] = 0
    m[1][0] = 0
    m[1][1] = 0
    m[1][2] = 1  # Message sent from e1(2) to e2(3)
    m[2][0] = 0
    m[2][1] = 0
    m[2][2] = 0
    m[3][0] = 0
    m[3][1] = 0
    m[3][2] = 0
    m[4][0] = 0
    m[4][1] = -1  # Message received at e1(5) from e2(3)
    m[4][2] = 0

    # Run Lamport's Logical Clock algorithm
    lamportLogicalClock(e1, e2, m)
