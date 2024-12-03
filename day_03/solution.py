import re


def mul(x, y):
    return x * y


if __name__ == "__main__":
    with open("day_03/input.txt") as f:
        mem = f.read()

    # PART 1
    print(f"PART 1: {sum(eval(exp) for exp in re.findall(r"mul\(\d+,\d+\)", mem))}")

    # PART 2
    total = 0
    enabled = True
    for exp in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", mem):
        if exp == "don't()":
            enabled = False
        elif exp == "do()":
            enabled = True
            continue

        if not enabled:
            continue
        total += eval(exp)

    print(f"PART 2: {total}")
