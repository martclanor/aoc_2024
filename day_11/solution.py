from functools import cache


def blink(stone: str) -> str:
    if stone == "0":
        return "1"
    elif (len_digits := len(stone)) % 2 == 0:
        return f"{int(stone[:len_digits // 2])} {int(stone[len_digits // 2:])}"
    else:
        return f"{int(stone) * 2024}"


@cache
def dfs(stones: str, n: int) -> int:
    if n == 0:
        return 2 if " " in stones else 1
    return sum(dfs(blink(stone), n - 1) for stone in stones.split())


if __name__ == "__main__":
    with open("day_11/input.txt") as f:
        stones = f.read().strip()
    print(f"PART 1: {dfs(stones, 25)}")
    print(f"PART 2: {dfs(stones, 75)}")
