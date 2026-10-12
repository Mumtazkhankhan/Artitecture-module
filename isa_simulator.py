"""Tiny educational ISA/CPU simulator. Run: python isa_simulator.py"""

class SimpleCPU:
    def __init__(self):
        self.registers = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
        self.memory = [0] * 16
        self.zero_flag = False
        self.pc = 0
        self.running = True

    def value(self, token):
        token = token.upper()
        return self.registers[token] if token in self.registers else int(token)

    def check_register(self, name):
        if name not in self.registers:
            raise ValueError(f"Unknown register {name}; use R0, R1, R2, or R3")

    def check_address(self, address):
        if not 0 <= address < len(self.memory):
            raise ValueError(f"Memory address must be 0 to {len(self.memory)-1}")

    def execute(self, instruction):
        parts = instruction.replace(",", " ").split()
        if not parts or parts[0].startswith("#"):
            self.pc += 1
            return
        op, *args = parts
        op = op.upper()
        args = [a.upper() for a in args]

        if op in ("MOV", "ADD", "SUB"):
            if len(args) != 2: raise ValueError(f"Wrong operands: {instruction}")
            dest = args[0]; self.check_register(dest)
            val = self.value(args[1])
            if op == "MOV": self.registers[dest] = val
            elif op == "ADD": self.registers[dest] += val
            else: self.registers[dest] -= val
            self.zero_flag = self.registers[dest] == 0
        elif op in ("INC", "DEC"):
            if len(args) != 1: raise ValueError(f"Wrong operands: {instruction}")
            reg = args[0]; self.check_register(reg)
            self.registers[reg] += 1 if op == "INC" else -1
            self.zero_flag = self.registers[reg] == 0
        elif op in ("LOAD", "STORE"):
            if len(args) != 2: raise ValueError(f"Wrong operands: {instruction}")
            reg, address_text = args
            self.check_register(reg)
            address = int(address_text); self.check_address(address)
            if op == "LOAD":
                self.registers[reg] = self.memory[address]
                self.zero_flag = self.registers[reg] == 0
            else:
                self.memory[address] = self.registers[reg]
        elif op == "JMP":
            if len(args) != 1: raise ValueError(f"Wrong operands: {instruction}")
            self.pc = int(args[0]); return
        elif op == "JZ":
            if len(args) != 1: raise ValueError(f"Wrong operands: {instruction}")
            if self.zero_flag:
                self.pc = int(args[0]); return
        elif op == "PRINT":
            if len(args) != 1: raise ValueError(f"Wrong operands: {instruction}")
            print(f"OUTPUT: {args[0]} = {self.value(args[0])}")
        elif op == "HALT":
            self.running = False
            return
        else:
            raise ValueError(f"Unknown instruction: {op}")
        self.pc += 1

    def run(self, program, max_steps=500):
        self.pc = 0; self.running = True; steps = 0
        print("\n--- Program execution ---")
        while self.running and 0 <= self.pc < len(program):
            if steps >= max_steps:
                raise RuntimeError("Step limit reached; check for an infinite loop")
            print(f"PC={self.pc:02}: {program[self.pc]}")
            self.execute(program[self.pc])
            steps += 1
        print("\n--- Final CPU state ---")
        print("Registers:", self.registers)
        print("Zero flag:", self.zero_flag)
        print("Memory:", self.memory)
        print("Instructions executed:", steps)

if __name__ == "__main__":
    program = [
        "MOV R0, 5",
        "MOV R1, 7",
        "ADD R0, R1",
        "STORE R0, 2",
        "LOAD R2, 2",
        "SUB R2, 2",
        "PRINT R2",
        "HALT"
    ]
    print("SIMPLE ISA / CPU SIMULATOR")
    print("Example program:")
    for i, line in enumerate(program): print(f"{i:02}: {line}")
    SimpleCPU().run(program)
