import random


class Participant:
    def __init__(self, name):
        self.name = name
        self.prepared = False
        self.committed = False

    def prepare(self):
        # Simulate the possibility of failure to prepare
        if random.choice([True, False]):
            print(f"{self.name}: Prepared to commit.")
            self.prepared = True
            return True
        else:
            print(f"{self.name}: Unable to prepare, aborting.")
            self.prepared = False
            return False

    def commit(self):
        if self.prepared:
            print(f"{self.name}: Committing.")
            self.committed = True
            return True
        return False

    def abort(self):
        print(f"{self.name}: Aborting transaction.")
        self.committed = False


class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def two_phase_commit(self):
        # Phase 1: Prepare
        print("Coordinator: Starting Phase 1 (Prepare)")
        for participant in self.participants:
            if not participant.prepare():
                print(
                    "Coordinator: One or more participants failed to prepare. Aborting."
                )
                self.abort_transaction()
                return False

        # Phase 2: Commit
        print("Coordinator: All participants are ready. Proceeding to commit.")
        for participant in self.participants:
            participant.commit()
        print("Coordinator: Transaction committed successfully.")
        return True

    def abort_transaction(self):
        print("Coordinator: Aborting transaction.")
        for participant in self.participants:
            participant.abort()


if __name__ == "__main__":
    participants = [Participant(f"Participant {i}") for i in range(3)]
    coordinator = Coordinator(participants)

    print("Starting 2-Phase Commit Protocol")
    result = coordinator.two_phase_commit()
    if result:
        print("Transaction completed successfully.")
    else:
        print("Transaction failed.")
