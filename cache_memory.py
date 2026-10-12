"""Educational cache simulator: direct mapped, FIFO, and LRU. Run: python cache_memory.py"""

class DirectMappedCache:
    def __init__(self, lines=4):
        if lines < 1:
            raise ValueError("Cache lines must be at least 1")
        self.lines = [None] * lines
        self.hits = self.misses = 0

    def access(self, block):
        index = block % len(self.lines)
        if self.lines[index] == block:
            self.hits += 1
            result = "HIT"
        else:
            self.misses += 1
            self.lines[index] = block
            result = "MISS"
        print(f"Block {block:>3} -> line {index}: {result}; cache={self.lines}")

    def report(self, title):
        total = self.hits + self.misses
        rate = self.hits / total * 100 if total else 0
        print(f"\n{title}: hits={self.hits}, misses={self.misses}, "
              f"hit rate={rate:.2f}%, miss rate={100-rate:.2f}%")

class FullyAssociativeCache:
    def __init__(self, capacity=4, policy="LRU"):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.policy = policy.upper()
        if self.policy not in ("FIFO", "LRU"):
            raise ValueError("Policy must be FIFO or LRU")
        self.blocks = []
        self.last_used = {}
        self.clock = 0
        self.hits = self.misses = 0

    def access(self, block):
        self.clock += 1
        if block in self.blocks:
            self.hits += 1
            self.last_used[block] = self.clock
            result = "HIT"
        else:
            self.misses += 1
            if len(self.blocks) >= self.capacity:
                if self.policy == "FIFO":
                    old = self.blocks.pop(0)
                else:
                    old = min(self.blocks, key=lambda item: self.last_used[item])
                    self.blocks.remove(old)
                self.last_used.pop(old, None)
            self.blocks.append(block)
            self.last_used[block] = self.clock
            result = "MISS"
        print(f"Block {block:>3}: {result}; cache={self.blocks}")

    def report(self):
        total = self.hits + self.misses
        rate = self.hits / total * 100 if total else 0
        print(f"\nFully associative {self.policy}: hits={self.hits}, misses={self.misses}, "
              f"hit rate={rate:.2f}%, miss rate={100-rate:.2f}%")

if __name__ == "__main__":
    print("CACHE MEMORY SIMULATOR (educational simulation)")
    raw = input("Enter block numbers separated by spaces, or press Enter for example: ").strip()
    try:
        refs = [int(x) for x in raw.split()] if raw else [0,1,2,3,0,4,0,1,5,2,3,4]
        if any(x < 0 for x in refs):
            raise ValueError
    except ValueError:
        print("Invalid input; using example reference string.")
        refs = [0,1,2,3,0,4,0,1,5,2,3,4]
    print("Reference string:", refs)

    direct = DirectMappedCache(4)
    print("\n--- Direct mapped (4 lines) ---")
    for b in refs: direct.access(b)
    direct.report("Direct mapped")

    fifo = FullyAssociativeCache(4, "FIFO")
    print("\n--- Fully associative FIFO (4 slots) ---")
    for b in refs: fifo.access(b)
    fifo.report()

    lru = FullyAssociativeCache(4, "LRU")
    print("\n--- Fully associative LRU (4 slots) ---")
    for b in refs: lru.access(b)
    lru.report()
