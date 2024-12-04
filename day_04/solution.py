from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Direction:
    x: int
    y: int


class Directions(Enum):
    e = Direction(1, 0)
    w = Direction(-1, 0)
    n = Direction(0, 1)
    s = Direction(0, -1)
    ne = Direction(1, 1)
    sw = Direction(-1, -1)
    se = Direction(1, -1)
    nw = Direction(-1, 1)


class DiagonalDirections(Enum):
    diag_1 = Direction(1, 1), Direction(-1, -1)
    diag_2 = Direction(1, -1), Direction(-1, 1)


def is_out(x, y):
    return x == length or y == length or x < 0 or y < 0


if __name__ == "__main__":
    with open("day_04/input.txt") as f:
        grid = [list(x.strip("\n")) for x in f.readlines()]

    length = len(grid)
    assert len(grid) == len(grid[0])  # Check if square grid

    # PART 1
    n_xmas = 0
    for y_x, row in enumerate(grid):
        for x_x, char in enumerate(row):
            if char != "X":
                continue

            for d in Directions:
                y_m = y_x + d.value.y
                x_m = x_x + d.value.x
                if is_out(x_m, y_m):
                    continue
                if grid[y_m][x_m] != "M":
                    continue

                y_a = y_m + d.value.y
                x_a = x_m + d.value.x
                if is_out(x_a, y_a):
                    continue
                if grid[y_a][x_a] != "A":
                    continue

                y_s = y_a + d.value.y
                x_s = x_a + d.value.x
                if is_out(x_s, y_s):
                    continue
                if grid[y_s][x_s] != "S":
                    continue

                n_xmas += 1

    print(f"PART 1: {n_xmas}")

    # PART 2
    n_xmas = 0
    for y_a, row in enumerate(grid):
        for x_a, char in enumerate(row):
            # Find center of "X" patterns
            if char != "A":
                continue

            for d in DiagonalDirections:
                y_1, y_2 = y_a + d.value[0].y, y_a + d.value[1].y
                x_1, x_2 = x_a + d.value[0].x, x_a + d.value[1].x

                if is_out(x_1, y_1) or is_out(x_2, y_2):
                    break
                chars = grid[y_1][x_1], grid[y_2][x_2]

                if "M" in chars and "S" in chars:
                    continue
                break  # diagonal is not "MAS"
            else:
                n_xmas += 1

    print(f"PART 2: {n_xmas}")
