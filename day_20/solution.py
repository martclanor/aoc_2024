from heapq import heappop, heappush

import numpy as np

from day_16.solution import Dir, Pos


def dijkstra_find_max_path(grid):
    while pq:
        dist, pos, direction, path = heappop(pq)

        path.add((pos, dist))
        if grid[pos.r, pos.c] == "E":
            return {p[0]: p[-1] for p in path}

        for direction_n in (direction, direction.turn_l(), direction.turn_r()):
            if ((pos_n := pos + direction_n), (dist_n := dist + 1)) in path:
                continue
            if grid[pos_n.r, pos_n.c] != "#":
                heappush(pq, (dist_n, pos_n, direction_n, path))


def dijkstra_count_cheats(grid):
    n_cheats = 0
    while pq:
        dist, pos, direction, path, cheated = heappop(pq)

        path.add((pos, dist))
        if grid[pos.r, pos.c] == "E":
            n_cheats += 1
            continue

        for direction_n in (direction, direction.turn_l(), direction.turn_r()):
            if ((pos_n := pos + direction_n), (dist_n := dist + 1)) in path:
                continue

            if pos_n in longest_path and cheated:
                heappush(pq, (dist_n, pos_n, direction_n, path.copy(), cheated))
                continue

            if grid[pos_n.r, pos_n.c] != "#":
                heappush(pq, (dist_n, pos_n, direction_n, path.copy(), cheated))
            else:
                if cheated:
                    continue
                if 0 > pos_n.r or size <= pos_n.r or 0 > pos_n.c or size <= pos_n.c:
                    continue
                pos_n_n = pos_n + direction_n
                if (
                    0 > pos_n_n.r
                    or size <= pos_n_n.r
                    or 0 > pos_n_n.c
                    or size <= pos_n_n.c
                ):
                    continue
                if grid[pos_n_n.r, pos_n_n.c] == "#":
                    continue
                dist_n_n = dist_n + 1

                # Compare amount of saved time with longest path
                if longest_path[pos_n_n] - dist_n_n >= 100:
                    heappush(pq, (max_dist, pos_end, direction_n, path, True))

    return n_cheats


if __name__ == "__main__":
    with open("day_20/input.txt") as f:
        grid = np.array([list(line.strip()) for line in f.readlines()])

    size = grid.shape[0]
    pos_start = Pos(*(int(n[0]) for n in np.where(grid == "S")))
    dir_start = Dir(0, 1)  # Start going East
    pos_end = Pos(*(int(n[0]) for n in np.where(grid == "E")))

    # PART 1
    # Setup priority queue: (cost, pos, direction, path)
    pq = [(0, pos_start, dir_start, set())]
    # Find path without cheating
    longest_path = dijkstra_find_max_path(grid)
    max_dist = len(longest_path) - 1

    # Setup priority queue: (cost, pos, direction, path, cheated)
    pq = [(0, pos_start, dir_start, set(), False)]
    n_cheats = dijkstra_count_cheats(grid) - 1
    print(f"PART 1:{n_cheats}")
