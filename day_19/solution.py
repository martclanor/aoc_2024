from collections import deque
from functools import cache


def count_possible_designs(display, patterns):
    disp = ""
    while display:
        # Take left most char one at a time, append to compare more chars after a loop
        disp += display.popleft()

        if len(disp) > max_len:  # Exit if already greater than max length of pattern
            break

        for pat in patterns:
            if disp == pat:
                if len(display) == 0:
                    return True
                if count_possible_designs(display.copy(), patterns):
                    return True
    return False


@cache
def count_ways_per_design(display, patterns, ways=0):
    # Convert to deque inside func for hashability
    display = deque(display)
    disp = ""
    while display:
        disp += display.popleft()

        if len(disp) > max_len:
            break

        for pat in patterns:
            if disp == pat:
                if len(display) == 0:
                    ways += 1
                else:
                    ways += count_ways_per_design("".join(display.copy()), patterns, 0)

    return ways


if __name__ == "__main__":
    with open("day_19/input.txt") as f:
        _patterns, _displays = f.read().split("\n\n")

    pats = tuple(p.strip() for p in _patterns.split(","))
    max_len = max(len(pattern) for pattern in pats)

    # PART 1
    disps = [deque(d) for d in _displays.strip().split("\n")]
    print(f"PART 1: {sum(count_possible_designs(disp, pats) for disp in disps)}")

    # PART 2
    disps = [d for d in _displays.strip().split("\n")]
    print(f"PART 2: {sum(count_ways_per_design(display, pats) for display in disps)}")
