from collections import Counter

if __name__ == "__main__":
    with open("day_01/input.txt") as f:
        left, right = zip(*[map(int, line.split()) for line in f.read().splitlines()])

    # PART 1
    distance = sum(abs(i - j) for i, j in zip(sorted(left), sorted(right)))
    print(f"PART 1: {distance}")

    # PART 2
    multiplier = Counter(right)
    similarity_score = sum(i * multiplier[i] for i in left)
    print(f"PART 2: {similarity_score}")
