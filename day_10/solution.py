import numpy as np


def is_out(row, col):
    return row < 0 or col < 0 or row >= height or col >= width


def is_traversed(traversed, row, col):
    return (row, col) in traversed


def dfs(grid, row, col, elev, traversed, part):
    if is_out(row, col):
        return 0
    if is_traversed(traversed, row, col):
        return 0
    if grid[row, col] != elev:
        return 0

    traversed.add((row, col))

    if grid[row, col] == 9:
        return 1

    if part == 2:
        # Allow each child to search independently from one another
        traversed = traversed.copy()
    return (
        # Search neighbors for the next elevation
        dfs(grid, row, col + 1, elev + 1, traversed, part)
        + dfs(grid, row, col - 1, elev + 1, traversed, part)
        + dfs(grid, row + 1, col, elev + 1, traversed, part)
        + dfs(grid, row - 1, col, elev + 1, traversed, part)
    )


if __name__ == "__main__":
    with open("day_10/input.txt") as f:
        grid = np.genfromtxt(f, delimiter=1, dtype=int)
    trailheads = np.where(grid == 0)
    height, width = grid.shape

    score_1 = 0
    score_2 = 0
    for row, col in zip(*trailheads):
        score_1 += dfs(grid, row, col, 0, set(), part=1)
        score_2 += dfs(grid, row, col, 0, set(), part=2)
    print(f"PART 1: {score_1}")
    print(f"PART 2: {score_2}")
