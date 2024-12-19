from dataclasses import dataclass
from heapq import heappop, heappush

import numpy as np


@dataclass(frozen=True, slots=True)
class Dir:
    dr: int
    dc: int


@dataclass(frozen=True, slots=True)
class Pos:
    r: int
    c: int

    def __add__(self, dir):
        return Pos(self.r + dir.dr, self.c + dir.dc)

    def __lt__(self, other):
        # For sorting within heap
        return self.r < other.r

    def __repr__(self):
        return f"{self.r},{self.c}"

    def within(self, dims):
        return 0 <= self.r and 0 <= self.c and self.r < dims[0] and self.c < dims[1]


def dijkstra(grid):
    seen = set()
    pq = [(0, Pos(0, 0))]
    while pq:
        dist, pos = heappop(pq)
        if (pos.r + 1, pos.c + 1) == DIMS:
            return dist
        if pos in seen:
            continue
        seen.add(pos)

        for direction in (Dir(0, 1), Dir(0, -1), Dir(-1, 0), Dir(1, 0)):
            pos_n = pos + direction
            if not pos_n.within(DIMS):
                continue
            if grid[pos_n.r, pos_n.c] == 0:
                continue
            heappush(pq, ((dist + 1), pos_n))


if __name__ == "__main__":
    with open("day_18/input.txt") as f:
        positions = [Pos(*map(int, line.strip().split(","))) for line in f.readlines()]

    DIMS = (71, 71)

    # PART 1
    grid = np.ones(DIMS, dtype=int)  # 1: good memory
    # Let first 1024 bytes to fall
    for pos in positions[:1024]:
        grid[pos.r, pos.c] = 0  # 0: corrupted memory
    print(f"PART 1: {dijkstra(grid)}")

    # PART 2
    grid = np.ones(DIMS, dtype=int)
    # Let all bytes to fall
    for pos in positions:
        grid[pos.r, pos.c] = 0

    # Fix each corrupted byte one at a time starting from the end
    for i, pos in enumerate(reversed(positions)):
        n = len(positions) - i
        grid[pos.r, pos.c] = 1
        if dijkstra(grid) is None:
            continue
        break
    print(f"PART 2: {positions[n-1]}")
