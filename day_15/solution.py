from dataclasses import dataclass
from enum import Enum

import numpy as np


@dataclass
class Grid:
    data: np.array

    def start(self):
        ind = np.where(self.data == "@")
        start_pos = int(ind[0][0]), int(ind[1][0])

        # Remove robot from start position
        self.data[start_pos] = "."

        return Pos(*start_pos)

    def sum_gps_coords1(self):
        return np.sum(
            np.where(self.data == "O")[0] * 100 + np.where(self.data == "O")[1]
        )

    def sum_gps_coords2(self):
        return np.sum(
            np.where(self.data == "[")[0] * 100 + np.where(self.data == "[")[1]
        )

    def widen(self):
        grid_l = self.data.copy()
        grid_r = self.data.copy()

        grid_l[grid_l == "O"] = "["
        grid_r[grid_r == "O"] = "]"
        grid_r[grid_r == "@"] = "."

        grid_l
        grid_r
        grid_new = np.empty((grid_l.shape[0], grid_l.shape[1] * 2), dtype=grid_l.dtype)
        grid_new[:, 0::2] = grid_l
        grid_new[:, 1::2] = grid_r

        self.data = grid_new


@dataclass
class Dir:
    dr: int
    dc: int


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __lt__(self, other):
        return self.r < other.r


class Move(Enum):
    n = Dir(-1, 0)
    s = Dir(1, 0)
    e = Dir(0, 1)
    w = Dir(0, -1)


def get_pos_box_pair(char, pos_box):
    if char == "[":
        return {pos_box, Pos(pos_box.r, pos_box.c + 1)}
    if char == "]":
        return {pos_box, Pos(pos_box.r, pos_box.c - 1)}


def get_next_pos_boxes(pos_boxes, direction):
    new_pos_boxes = set()
    for pos_box in pos_boxes:
        try:
            for pb in get_pos_box_pair(
                grid.data[pos_box.r + direction.dr, pos_box.c + direction.dc], pos_box
            ):
                new_pos_boxes.add(Pos(pb.r + direction.dr, pb.c + direction.dc))
        except TypeError:
            continue
    return new_pos_boxes


if __name__ == "__main__":
    with open("day_15/input.txt") as f:
        _grid, _moves = f.read().split("\n\n")
        grid = Grid(np.array([list(g) for g in _grid.split("\n")]))
        moves = tuple("".join(_moves.split("\n")))

    move_dir = {
        "^": Move.n.value,
        "v": Move.s.value,
        ">": Move.e.value,
        "<": Move.w.value,
    }

    # PART 1
    robot_pos = grid.start()  # Note robot_position, remove robot
    for move in moves:
        direction = move_dir[move]
        char = grid.data[
            r_n := robot_pos.r + direction.dr, c_n := robot_pos.c + direction.dc
        ]

        # Robot moves to a wall
        if char == "#":
            continue
        # Robot moves to a space
        elif char == ".":
            robot_pos = Pos(r_n, c_n)

        # Robot moves to a box
        elif char == "O":
            pos = Pos(r_n, c_n)
            box_1 = Pos(r_n, c_n)
            # Check if there's any space behind the box
            while True:
                char = grid.data[
                    r_n := pos.r + direction.dr, c_n := pos.c + direction.dc
                ]
                # No space behind box
                if char == "#":
                    break

                pos = Pos(r_n, c_n)

                # Space behind box found
                if char == ".":
                    robot_pos = Pos(box_1.r, box_1.c)
                    # Remove box_1
                    grid.data[box_1.r, box_1.c] = "."
                    # Add new box_1
                    grid.data[r_n, c_n] = "O"
                    break

    print(f"PART 1: {grid.sum_gps_coords1()}")

    # PART 2
    grid = Grid(np.array([list(g) for g in _grid.split("\n")]))
    grid.widen()

    robot_pos = grid.start()  # Note robot_position, remove robot
    for i, move in enumerate(moves):
        direction = move_dir[move]
        char = grid.data[
            r_n := robot_pos.r + direction.dr, c_n := robot_pos.c + direction.dc
        ]

        # Robot moves to a wall
        if char == "#":
            continue
        # Robot moves to a space
        elif char == ".":
            robot_pos = Pos(r_n, c_n)

        # Robot moves to a box horizontally
        elif move in ("<", ">") and char in ("[", "]"):
            box_1a = Pos(r_n, c_n)
            pos_boxes = []  # Collect boxes positions
            box_1b = Pos(r_n := r_n + direction.dr, c_n := c_n + direction.dc)
            pos_boxes.append(box_1b)
            pos = Pos(box_1b.r, box_1b.c)
            # Check if there's any space behind the box
            while True:
                char = grid.data[
                    r_n := pos.r + direction.dr, c_n := pos.c + direction.dc
                ]
                # No space behind box
                if char == "#":
                    break

                # Just another box
                if char in ("[", "]"):
                    pos_boxes.append(Pos(r_n, c_n))
                    pos = Pos(
                        r_n + direction.dr, c_n + direction.dc
                    )  # Move another space
                    pos_boxes.append(pos)
                    continue

                # Space behind box found
                if char == ".":
                    robot_pos = Pos(box_1a.r, box_1a.c)
                    # Add new box at the end
                    grid.data[r_n, c_n] = grid.data[box_1a.r, box_1a.c]
                    pos_boxes.append(Pos(r_n, c_n))

                    # Remove box_1a
                    grid.data[box_1a.r, box_1a.c] = "."

                    # Finally, flip all boxes to correct orientation
                    for pos_box in pos_boxes:
                        if grid.data[pos_box.r, pos_box.c] == "[":
                            grid.data[pos_box.r, pos_box.c] = "]"
                        elif grid.data[pos_box.r, pos_box.c] == "]":
                            grid.data[pos_box.r, pos_box.c] = "["
                    break

        # Robot moves to a box vertically
        elif move in ("^", "v") and char in ("[", "]"):
            box_1a = Pos(r_n, c_n)
            pos_boxes = set()
            pos_boxes_per_row = get_pos_box_pair(char, Pos(r_n, c_n))
            wall_exists = False
            all_spaces = False

            while True:
                pos_boxes.update(pos_boxes_per_row)
                chars = set()
                for pos_box in pos_boxes_per_row:
                    chars.add(
                        grid.data[pos_box.r + direction.dr, pos_box.c + direction.dc]
                    )

                # Wall exists
                if any(c == "#" for c in chars):
                    wall_exists = True
                    break

                # All spaces
                if all(c == "." for c in chars):
                    all_spaces = True
                    break

                pos_boxes_per_row = get_next_pos_boxes(pos_boxes_per_row, direction)

            if all_spaces:
                if direction.dr > 0:
                    sorted_pos_boxes = reversed(sorted(pos_boxes))
                else:
                    sorted_pos_boxes = sorted(pos_boxes)

                for pos_box in sorted_pos_boxes:
                    c = grid.data[pos_box.r, pos_box.c]
                    grid.data[pos_box.r, pos_box.c] = "."
                    grid.data[pos_box.r + direction.dr, pos_box.c + direction.dc] = c
                robot_pos = Pos(box_1a.r, box_1a.c)

    print(f"PART 2: {grid.sum_gps_coords2()}")

    # Check
    print(move)
    print(robot_pos)
    test_grid = grid.data.copy()
    test_grid[robot_pos.r, robot_pos.c] = "@"
    for line in range(test_grid.shape[0]):
        print("".join(list(test_grid[line])))
