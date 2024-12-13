from dataclasses import dataclass

import numpy as np


@dataclass(slots=True, frozen=True)
class Plot:
    data: tuple

    @property
    def fences(self):
        return {
            Fence(self.data[1], self.data[0], "we"),
            Fence(self.data[1], self.data[0] + 1, "we"),
            Fence(self.data[0], self.data[1], "ns"),
            Fence(self.data[0], self.data[1] + 1, "ns"),
        }


@dataclass
class Region:
    plant: str
    plots: set[Plot]

    @classmethod
    def from_garden_group(cls, key, values):
        return cls(key[0], {Plot(value) for value in values})

    @property
    def fences(self):
        fences = set()
        for plot in self.plots:
            # Shared fences between plots are dissolved
            fences = fences ^ plot.fences
        return fences

    @property
    def area(self):
        return len(self.plots)

    @property
    def perimeter(self):
        return len(self.fences)

    @staticmethod
    def groupby(fences, key):
        if key == "direction":
            return [fence for fence in fences if fence.direction == "ns"], [
                fence for fence in fences if fence.direction == "we"
            ]
        elif key == "space_id":
            grouped = {}
            for fence in fences:
                if fence.space_id in grouped:
                    grouped[fence.space_id].add(fence)
                    continue
                grouped[fence.space_id] = {fence}
            return list(grouped.values())

    @staticmethod
    def count_sides(fences):
        """For each 'construction line', count the number of unconnected fence."""
        count = 0
        for f, fence in enumerate(sorted(fences)):
            if fence.direction == "we":
                if (r := fence.space_id - 1) >= 0 and garden[
                    r, fence.pos
                ] == region.plant:
                    side = "left"
                elif garden[fence.space_id, fence.pos] == region.plant:
                    side = "right"
            elif fence.direction == "ns":
                if (c := fence.space_id - 1) >= 0 and garden[
                    fence.pos, c
                ] == region.plant:
                    side = "right"
                elif garden[fence.pos, fence.space_id] == region.plant:
                    side = "left"

            if f == 0:
                count += 1
                prev_pos, prev_side = fence.pos, side
                continue

            if prev_pos + 1 == fence.pos and prev_side == side:
                prev_pos, prev_side = fence.pos, side
                continue

            prev_pos, prev_side = fence.pos, side
            count += 1
        return count


@dataclass(slots=True, frozen=True)
class Fence:
    pos: int
    space_id: int
    direction: str

    def __lt__(self, other):
        return self.pos < other.pos


def is_out(row, col):
    return row < 0 or col < 0 or row >= height or col >= width


def is_checked(row, col):
    return (row, col) in checked


def dfs(row, col, plant, uid):
    if is_checked(row, col):
        return
    checked.add((row, col))

    if uid in groups:
        groups[uid].add((row, col))
    else:
        groups[uid] = {(row, col)}

    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        r = row + dr
        c = col + dc
        if is_out(r, c) or is_checked(r, c) or garden[(r, c)] != plant:
            continue
        dfs(r, c, plant, uid)


if __name__ == "__main__":
    with open("day_12/input.txt") as f:
        garden = np.genfromtxt(f, delimiter=1, dtype=None)

    groups = {}
    checked = set()
    checked = set()
    height, width = garden.shape
    for row in range(height):
        for col in range(width):
            dfs(row, col, garden[row, col], f"{garden[row, col]} {row} {col}")

    regions = [Region.from_garden_group(*group) for group in groups.items()]

    # PART 1
    print(f"PART 1: {sum(region.area * region.perimeter for region in regions)}")

    # PART 2
    total = 0
    for region in regions:
        sides = 0
        for fences_direction in Region.groupby(region.fences, "direction"):
            for fence_space_id in Region.groupby(fences_direction, "space_id"):
                sides += Region.count_sides(fence_space_id)
        total += sides * region.area
    print(f"PART 2: {total}")
