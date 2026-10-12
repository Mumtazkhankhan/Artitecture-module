"""Educational I/O and Bus Architecture simulator. Runs on Windows with Python 3."""

class Bus:
    def __init__(self):
        self.data = None
        self.address = None
        self.control = "IDLE"

    def transfer(self, address, data, operation="WRITE"):
        self.address = address
        self.control = operation.upper()
        if self.control not in ("READ", "WRITE"):
            raise ValueError("Operation must be READ or WRITE")
        if self.control == "WRITE":
            self.data = data
            return f"Bus WRITE: address={self.address}, data={self.data}, control={self.control}"
        return f"Bus READ: address={self.address}, data={self.data}, control={self.control}"


def main():
    bus = Bus()
    device_memory = {100: "Keyboard input: A", 200: "Display ready"}
    print("I/O and Bus Architecture Simulator")
    print(bus.transfer(100, device_memory[100], "WRITE"))
    print(bus.transfer(200, device_memory[200], "WRITE"))
    print("\nBus parts demonstrated: address, data, and control signals.")
    print("This is a simple software model, not a real hardware bus.")


if __name__ == "__main__":
    main()
