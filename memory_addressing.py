"""Educational Memory and Addressing simulator. Runs on Windows with Python 3."""

MEMORY_SIZE = 16


def resolve_address(mode, operand, registers, memory):
    mode = mode.lower()
    if mode == "immediate":
        return None, int(operand)
    if mode == "direct":
        address = int(operand)
        return address, memory[address]
    if mode == "register":
        return None, registers[operand.upper()]
    if mode == "indirect":
        address = registers[operand.upper()]
        return address, memory[address]
    raise ValueError("Mode must be immediate, direct, register, or indirect")


def main():
    memory = [0] * MEMORY_SIZE
    memory[5] = 42
    registers = {"R0": 5, "R1": 9}
    print("Memory and Addressing Simulator")
    print("Memory cell 5 contains 42; R0 contains address 5; R1 contains 9.\n")
    tests = [("immediate", "12"), ("direct", "5"), ("register", "R1"), ("indirect", "R0")]
    for mode, operand in tests:
        address, value = resolve_address(mode, operand, registers, memory)
        if address is None:
            print(f"{mode.title()} addressing, operand {operand}: value = {value}")
        else:
            print(f"{mode.title()} addressing, address {address}: value = {value}")
    print("\nThis is a teaching simulation, not actual physical memory access.")


if __name__ == "__main__":
    main()
