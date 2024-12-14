from dataclasses import dataclass
from math import prod
from typing import ClassVar

import numpy as np
from PIL import Image


@dataclass(slots=True)
class Pos:
    r: int
    c: int

    def move(self, velo, secs=1):
        return Pos(
            (self.r + velo.dr * secs) % height,
            (self.c + velo.dc * secs) % width,
        )


@dataclass(slots=True)
class Velo:
    dr: int
    dc: int


@dataclass(slots=True)
class Vector:
    pos: Pos
    velo: Velo

    @classmethod
    def from_line(cls, line):
        return cls(
            pos=Pos(*map(int, reversed((line.split()[0].split("=")[-1].split(","))))),
            velo=Velo(*map(int, reversed((line.split("=")[-1]).split(",")))),
        )

    def move(self, secs):
        return self.pos.move(self.velo, secs)


@dataclass
class Grid:
    q1: ClassVar[int] = 0
    q2: ClassVar[int] = 0
    q3: ClassVar[int] = 0
    q4: ClassVar[int] = 0

    def __post_init__(self):
        self.data = np.zeros((height, width), dtype=np.int32)

    def count_per_q(self, r, c):
        if r <= (height // 2 - 1) and c <= (width // 2 - 1):
            Grid.q1 += 1
        if r <= (height // 2 - 1) and (width // 2 + 1) <= c <= (width - 1):
            Grid.q2 += 1
        if (height // 2 + 1) <= r <= (height - 1) and c <= (width // 2 - 1):
            Grid.q3 += 1
        if (height // 2 + 1) <= r <= (height - 1) and (width // 2 + 1) <= c <= (
            width - 1
        ):
            Grid.q4 += 1

    @staticmethod
    def start(data, positions):
        for pos in positions:
            data[pos.r, pos.c] += 1
        return data

    @staticmethod
    def simulate(data, positions, velocities):
        new_positions = []
        for pos, velo in zip(positions, velocities):
            # Disappear from pos
            if data[pos.r, pos.c] - 1 < 0:
                data[pos.r, pos.c] = 0
            else:
                data[pos.r, pos.c] -= 1
            # Appear in pos + velo, collect new pos
            new_positions.append(new_pos := pos.move(velo))
            data[new_pos.r, new_pos.c] += 1
        return data, new_positions


if __name__ == "__main__":
    with open("day_14/input.txt") as f:
        vectors = [Vector.from_line(line.strip()) for line in f.readlines()]

    height, width = 103, 101

    # PART 1
    # Per vector, simulate move for 100 secs, then add to corresponding quadrant count
    _ = [Grid().count_per_q(v.move(100).r, v.move(100).c) for v in vectors]
    print(f"PART 1: {prod((Grid.q1, Grid.q2, Grid.q3, Grid.q4))}")

    # PART 2
    grid = Grid()
    positions, velocities = zip(*[(vector.pos, vector.velo) for vector in vectors])
    data = grid.start(grid.data, positions)

    # Per timestep, simulate move for all vectors, save array and positions
    for i in range(1, 10_000):
        # Overwrite array and positions for each move
        data, positions = Grid.simulate(data, positions, velocities)

        # Normalize data to plot as uint8
        normalized_data = (data - data.min()) * (255 / (data.max() - data.min()))
        image = Image.fromarray(normalized_data.astype(np.uint8))
        image.save(f"./day_14/{i:04}.png")
    print("PART 2: FIND THE X-MAS tree on the exported images! :D")
