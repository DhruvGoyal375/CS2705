import time
import random


class Participant:
    def __init__(self, name):
        self.name = name
        self.state = (
            "INITIAL"  # Possible states: INITIAL, READY, PRECOMMIT, COMMIT, ABORT
        )

    def can_commit(self):
        # Simulate the decision to prepare
        if random.choice([True, False]):
            print(f"{self.name}: Can commit (ready).")
            self.state = "READY"
            return True
        else:
            print(f"{self.name}: Cannot commit, aborting.")
            self.state = "ABORT"
            return False

    def pre_commit(self):
        if self.state == "READY":
            print(f"{self.name}: Pre-committing.")
            self.state = "PRECOMMIT"
            return True
        return False

    def do_commit(self):
        if self.state == "PRECOMMIT":
            print(f"{self.name}: Committing.")
            self.state = "COMMIT"
            return True
        return False

    def abort(self):
        print(f"{self.name}: Aborting transaction.")
        self.state = "ABORT"


class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def three_phase_commit(self):
        # Phase 1: CanCommit
        print("Coordinator: Starting Phase 1 (CanCommit)")
        for participant in self.participants:
            if not participant.can_commit():
                print("Coordinator: One or more participants cannot commit. Aborting.")
                self.abort_transaction()
                return False

        # Phase 2: PreCommit
        print("Coordinator: All participants are ready. Starting Phase 2 (PreCommit)")
        for participant in self.participants:
            if not participant.pre_commit():
                print("Coordinator: Failed to enter PreCommit state. Aborting.")
                self.abort_transaction()
                return False

        # Simulate a delay or possible failure
        time.sleep(1)
        if random.choice([True, False]):
            print("Coordinator: Network or system failure. Aborting transaction.")
            self.abort_transaction()
            return False

        # Phase 3: DoCommit
        print(
            "Coordinator: All participants in PreCommit state. Starting Phase 3 (DoCommit)"
        )
        for participant in self.participants:
            if not participant.do_commit():
                print(
                    "Coordinator: One or more participants failed to commit. Aborting."
                )
                self.abort_transaction()
                return False

        print("Coordinator: Transaction committed successfully.")
        return True

    def abort_transaction(self):
        print("Coordinator: Aborting transaction.")
        for participant in self.participants:
            participant.abort()


if __name__ == "__main__":
    participants = [Participant(f"Participant {i}") for i in range(3)]
    coordinator = Coordinator(participants)

    print("Starting 3-Phase Commit Protocol")
    result = coordinator.three_phase_commit()
    if result:
        print("Transaction completed successfully.")
    else:
        print("Transaction failed.")
