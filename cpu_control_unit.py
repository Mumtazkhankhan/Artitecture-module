"""Educational CPU Design and Control Unit simulator. Runs on Windows with Python 3."""

REGISTERS = {f"R{i}": 0 for i in range(4)}


def execute(instruction, registers):
    """Execute one simple instruction and return a human-readable control signal trace."""
    parts = instruction.upper().replace(',', ' ').split()
    if not parts:
        return "No instruction"
    op, *args = parts
    signals = []
    if op == "MOV" and len(args) == 2:
        dest, source = args
        value = registers[source] if source in registers else int(source)
        signals = ["Instruction Register: MOV", "Control Unit: decode MOV", "ALU: bypass", f"Register Write Enable: {dest}"]
        registers[dest] = value
    elif op in ("ADD", "SUB") and len(args) == 2:
        dest, source = args
        value = registers[source] if source in registers else int(source)
        signals = [f"Instruction Register: {op}", f"ALU: {op} {registers[dest]} and {value}", f"Register Write Enable: {dest}"]
        registers[dest] = registers[dest] + value if op == "ADD" else registers[dest] - value
    elif op == "INC" and len(args) == 1:
        dest = args[0]
        signals = ["Control Unit: decode INC", "ALU: increment", f"Register Write Enable: {dest}"]
        registers[dest] += 1
    elif op == "PRINT" and len(args) == 1:
        dest = args[0]
        signals = ["Control Unit: decode PRINT", "Output Enable: ON"]
        signals.append(f"OUTPUT: {dest} = {registers[dest]}")
    else:
        raise ValueError(f"Invalid instruction: {instruction}")
    return "\n".join(signals)


def main():
    registers = {f"R{i}": 0 for i in range(4)}
    program = ["MOV R0, 7", "MOV R1, 3", "ADD R0, R1", "INC R0", "PRINT R0"]
    print("CPU Design and Control Unit Simulator")
    print("Initial registers:", registers)
    for instruction in program:
        print(f"\nInstruction: {instruction}")
        print(execute(instruction, registers))
    print("\nFinal registers:", registers)


if __name__ == "__main__":
    main()
