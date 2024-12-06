from dataclasses import dataclass
from enum import Enum
from itertools import cycle


@dataclass(frozen=True)
class Direction:
    x: int
    y: int


class Directions(Enum):
    n = Direction(0, -1)
    e = Direction(1, 0)
    s = Direction(0, 1)
    w = Direction(-1, 0)


def is_out(x, y):
    return x == width or y == height or x < 0 or y < 0


if __name__ == "__main__":
    with open("day_06/input.txt") as f:
        grid = [list(line.strip("\n")) for line in f.readlines()]

    # Find guard starting position
    for y, row in enumerate(grid):
        for x, guard in enumerate(row):
            if guard == "^":
                break
        if guard == "^":
            break
    x_start = x
    y_start = y

    height = len(grid)
    width = len(grid[0])

    # PART 1
    positions = []
    out_of_bounds = False
    x = x_start
    y = y_start
    for direction in cycle(Directions):
        while True:
            if is_out((x_n := x + direction.value.x), (y_n := y + direction.value.y)):
                out_of_bounds = True
                break
            if grid[y_n][x_n] == "#":
                break
            x, y = x_n, y_n
            positions.append((x_n, y_n))
        if out_of_bounds:
            break
    positions_orig = set(positions)
    print(f"PART 1: {len(positions_orig) + 1}")

    # PART 2
    # Brute force: replace each "." with a barrier and check for loops
    loop_count = 0
    for y_r, row in enumerate(grid):
        for x_r, char in enumerate(row):
            # If not in the original path, ignore, no effect
            if (x_r, y_r) not in positions_orig:
                continue
            if char != ".":
                continue

            # Place barrier
            grid[y_r][x_r] = "#"
            # Set conditions before start of each loop check
            loop = False
            out_of_bounds = False
            positions = []
            x = x_start
            y = y_start

            for direction in cycle(Directions):
                while True:
                    if is_out(
                        (x_n := x + direction.value.x), (y_n := y + direction.value.y)
                    ):
                        out_of_bounds = True
                        break
                    if grid[y_n][x_n] == "#":
                        break
                    # Check if location is traversed already in the same direction
                    if (x, y, direction.value) not in positions:
                        positions.append((x, y, direction.value))
                    else:
                        loop = True
                        break

                    # Set next x, y as current
                    x, y = x_n, y_n

                if out_of_bounds:
                    break
                if loop:
                    loop_count += 1
                    break

            # Remove barrier
            grid[y_r][x_r] = "."

        print(f"Row {y_r + 1} of {height}")

    print(f"PART 2: {loop_count}")
