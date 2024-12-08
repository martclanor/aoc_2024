from dataclasses import dataclass
from functools import cached_property
from itertools import combinations


@dataclass(slots=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_out(self):
        return self.x >= size or self.y >= size or self.x < 0 or self.y < 0


@dataclass(frozen=True)
class Pair:
    p1: Point
    p2: Point

    @classmethod
    def from_combi(cls, combi):
        return cls(Point(*combi[0]), Point(*combi[1]))

    @cached_property
    def dist(self):
        return self.p2 - self.p1

    def get_antinodes(self, part):
        if part == 1:
            return {
                p for p in [self.p1 - self.dist, self.p2 + self.dist] if not p.is_out()
            }

        antinodes = {p1 := self.p1, p2 := self.p2}  # Starting points are antinodes too
        # Walk through one side of line, if is_out, exit
        while True:
            if (p1 := p1 - self.dist).is_out():
                break
            antinodes.add(p1)
        # Walk through the other side of line
        while True:
            if (p2 := p2 + self.dist).is_out():
                break
            antinodes.add(p2)
        return antinodes


if __name__ == "__main__":
    with open("day_08/input.txt") as f:
        grid = [list(line.strip()) for line in f.readlines()]
    size = len(grid)

    # Get all frequencies and their corresponding locations
    freqs = {}
    for y, row in enumerate(grid):
        for x, freq in enumerate(row):
            if freq == ".":
                continue
            if freq not in freqs:
                freqs[freq] = []
            freqs[freq].append((x, y))

    antinodes_1 = set()
    antinodes_2 = set()
    for locs in freqs.values():
        for combi in combinations(locs, 2):
            pair = Pair.from_combi(combi)
            antinodes_1 |= pair.get_antinodes(part=1)
            antinodes_2 |= pair.get_antinodes(part=2)
    print(f"PART 1: {len(antinodes_1)}")
    print(f"PART 2: {len(antinodes_2)}")
