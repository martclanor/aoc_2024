from dataclasses import dataclass
from heapq import heappop, heappush

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

    def __lt__(self, other):
        # For sorting within heap
        return self.dr < other.dr

    def turn_l(self):
        return Dir(-self.dc, self.dr)

    def turn_r(self):
        return Dir(self.dc, -self.dr)


@dataclass(frozen=True, slots=True)
class Pos:
    r: int
    c: int

    def __add__(self, dir):
        return Pos(self.r + dir.dr, self.c + dir.dc)

    def __lt__(self, other):
        # For sorting within heap
        return self.r < other.r


def dijkstra(grid, min_dist=np.inf):
    seen = set()
    paths = set()

    while pq:
        dist, pos, direction, seats = heappop(pq)

        seats.add(pos)
        if (char := grid[pos.r, pos.c]) == "E":
            min_dist = min(min_dist, dist)
            paths.update(seats)
            continue

        if char == "#":
            continue

        seen.add((pos, direction))

        for (
            dist_n,
            pos_n,
            direction_n,
            turn,
        ) in zip(
            (dist + 1, dist + 1000, dist + 1000),
            (pos + direction, pos, pos),
            (direction, direction.turn_l(), direction.turn_r()),
            (False, True, True),
        ):
            if (pos_n, direction_n) in seen:
                continue
            if dist_n > min_dist:
                continue
            if turn and grid[(pos_n + direction_n).r, (pos_n + direction_n).c] != "#":
                # Traverse turns independently, copy seats
                heappush(pq, (dist_n, pos_n, direction_n, seats.copy()))
            if not turn and grid[pos_n.r, pos_n.c] != "#":
                heappush(pq, (dist_n, pos_n, direction_n, seats))

    return min_dist, paths


if __name__ == "__main__":
    with open("day_16/input.txt") as f:
        grid = np.array([list(line.strip()) for line in f.readlines()])

    pos_start = Pos(*(int(n[0]) for n in np.where(grid == "S")))
    dir_start = Dir(0, 1)  # Start going East

    # Setup priority queue: (cost, current pos, direction)
    pq = [(0, pos_start, dir_start, set())]

    min_dist, paths = dijkstra(grid)
    print(f"PART 1: {min_dist}")
    print(f"PART 2: {len(paths)}")

    # Check
    for pos in paths:
        grid[pos.r, pos.c] = "O"
    for line in range(grid.shape[0]):
        print("".join(list(grid[line])))
