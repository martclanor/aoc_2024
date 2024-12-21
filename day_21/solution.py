from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush
from itertools import product

import numpy as np


@dataclass(frozen=True, slots=True)
class Dir:
    dr: int
    dc: int

    def __repr__(self):
        # For easier debugging
        if self.dr == -1 and self.dc == 0:
            return "^"
        if self.dr == 1 and self.dc == 0:
            return "v"
        if self.dr == 0 and self.dc == 1:
            return ">"
        if self.dr == 0 and self.dc == -1:
            return "<"
        if self.dr == 0 and self.dc == 0:
            return "A"


class Directions(Enum):
    left = Dir(0, -1)
    down = Dir(1, 0)
    right = Dir(0, 1)
    up = Dir(-1, 0)


@dataclass(frozen=True, slots=True)
class Pos:
    r: int
    c: int

    def __add__(self, dir):
        return Pos(self.r + dir.dr, self.c + dir.dc)

    def __sub__(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)

    def __lt__(self, other):
        # For sorting within heap
        return self.r < other.r


@dataclass
class Keypad:
    grid: np.array

    def __post_init__(self):
        self.height, self.width = self.grid.shape

    def get_pos(self, char):
        return Pos(*(int(n[0]) for n in np.where(self.grid == char)))

    def is_blank(self, pos):
        return self.grid[pos.r, pos.c] == "B"

    def is_out(self, pos):
        return pos.r < 0 or pos.c < 0 or pos.r >= self.height or pos.c >= self.width

    def min_paths(self, code):
        paths = defaultdict(set)

        start = self.get_pos("A")
        for i, c in enumerate(code):
            end = self.get_pos(c)
            dist = start - end
            source = str(self.grid[start.r, start.c])

            pq = [(dist, start, "", deque())]
            while pq:
                dist, start, path, seen = heappop(pq)

                seen.append(start)

                if dist == 0:
                    paths[(i, source, c)].add(path + "A")
                    continue

                for direction in Directions:
                    step = start + direction.value
                    if step in seen:
                        continue
                    if self.is_out(step) or self.is_blank(step):
                        continue
                    # Step takes it one unit of distance closer
                    if end - step + 1 == dist:
                        heappush(
                            pq,
                            (dist - 1, step, path + str(direction.value), seen.copy()),
                        )

        return paths


if __name__ == "__main__":
    with open("day_21/input.txt") as f:
        codes = [line.strip() for line in f.readlines()]

    kp_n = Keypad(np.array([[7, 8, 9], [4, 5, 6], [1, 2, 3], ["B", 0, "A"]]))
    kp_3 = Keypad(np.array([["B", "^", "A"], ["<", "v", ">"]]))
    kp_2 = Keypad(np.array([["B", "^", "A"], ["<", "v", ">"]]))
    kp_1 = Keypad(np.array([["B", "^", "A"], ["<", "v", ">"]]))

    # PART 1
    total = 0
    for code in codes:
        min_length = 999_999
        # Brute force approach: find all paths for keypad 3 (next to numeric keypad)
        for code_kp_3 in (
            "".join(path) for path in product(*kp_n.min_paths(code).values())
        ):
            # Convert each kp 3 code to kp 2 code
            for code_kp_2 in (
                "".join(path) for path in product(*kp_3.min_paths(code_kp_3).values())
            ):
                # Convert each kp 2 code to kp 1 code, then take minimum length of code
                for code_kp_1 in (
                    "".join(path)
                    for path in product(*kp_2.min_paths(code_kp_2).values())
                ):
                    min_length = min(len(code_kp_1), min_length)

        total += min_length * int(code[:-1])
    print(f"PART 1: {total}")
