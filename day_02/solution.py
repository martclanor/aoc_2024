from itertools import pairwise

# Safe diffs
DIFFS_OK = (-1, -2, -3, 1, 2, 3)


def is_safe(report):
    sign = None
    for a, b in pairwise(report):
        diff = a - b
        if sign is None:
            if diff in DIFFS_OK:
                sign = "-" if diff in DIFFS_OK[:3] else "+"
            else:
                # First diff is bad
                return False
        else:
            if (sign == "-" and diff not in DIFFS_OK[:3]) or (
                sign == "+" and diff not in DIFFS_OK[3:]
            ):
                return False
    return True


if __name__ == "__main__":
    with open("day_02/input.txt") as f:
        reports = [list(map(int, line.split())) for line in f.readlines()]

    # PART 1
    print(f"PART 1: {sum(is_safe(report) for report in reports)}")

    # PART 2
    total_safe = 0
    for report in reports:
        # First, check safety while keeping original report
        if is_safe(report):
            total_safe += 1
            continue

        # Then, brute force approach: remove each element one at a time and check
        for index in range(len(report)):
            report_ = [n for i, n in enumerate(report) if i != index]
            if not is_safe(report_):
                continue
            total_safe += 1
            break

    print(f"PART 2: {total_safe}")
