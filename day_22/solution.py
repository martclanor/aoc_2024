from collections import defaultdict, deque
from functools import cached_property
from itertools import pairwise


class SecretNumber:
    hist = deque()

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return str(self.number)

    def mix(self, integer):
        return SecretNumber(self.number ^ integer)

    def prune(self):
        return SecretNumber(self.number % 16777216)

    def sequence_1(self):
        return SecretNumber(self.number * 64).mix(self.number).prune()

    def sequence_2(self):
        return SecretNumber(self.number // 32).mix(self.number).prune()

    def sequence_3(self):
        return SecretNumber(self.number * 2048).mix(self.number).prune()

    def evolve(self, times):
        sn = self
        self.hist.append(sn.number % 10)
        for _ in range(times):
            sn = sn.sequence_1().sequence_2().sequence_3()
            self.hist.append(sn.number % 10)
        return sn

    @cached_property
    def deltas(self):
        return [b - a for a, b in pairwise(self.hist)]

    @cached_property
    def deltas_str(self):
        return "".join(map(str, self.deltas))

    def reset_hist(self):
        SecretNumber.hist = deque()

    def get_strat(self, i):
        return "".join(map(str, self.deltas[(i - 4) : i]))


if __name__ == "__main__":
    with open("day_22/input.txt") as f:
        numbers = [int(s.strip()) for s in f.readlines()]

    # PART 1
    print(f"PART 1: {sum(SecretNumber(n).evolve(2000).number for n in numbers)}")

    # PART 2
    # For each possible strat, calculate total bananas
    strat_total = defaultdict(int)
    SecretNumber.hist = deque()
    for n, num in enumerate(numbers):
        sn = SecretNumber(num).evolve(2000)
        seen = set()
        for i, price in enumerate(sn.hist):
            if i < 4:
                # 4-char length strat not possible
                continue
            if (strat := sn.get_strat(i)) in seen:
                continue
            seen.add(strat)
            strat_total[strat] += price
        sn.reset_hist()
    print(f"PART 2: {strat_total[max(strat_total, key=strat_total.get)]}")
