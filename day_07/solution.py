from dataclasses import dataclass
from itertools import product


@dataclass
class Line:
    data: str

    def __post_init__(self):
        self.answer = int(self.data[0])
        self.terms = tuple(self.data[1].split())

    @property
    def n_ops(self):
        # Number of operations that can be inserted within self.terms
        return len(self.terms) - 1


def get_total_calib(op_group):
    total = 0
    for i, line in enumerate(lines):
        print(f"{i + 1} of {len(lines)}")
        for op in product(op_group, repeat=line.n_ops):
            for j, term in enumerate(line.terms, start=-1):
                # n_terms = n_ops + 1, skip first term
                if j == -1:
                    answer = term
                    continue
                # Update answer based on new operator and term
                # "".join(exp.split()) does the concatenate operation (" "), if needed
                answer = eval("".join(f"{answer}{op[j]}{term}".split()))
            if answer == line.answer:
                total += answer
                break
    return total


if __name__ == "__main__":
    with open("day_07/input.txt") as f:
        lines = [Line(data.strip("\n").split(": ")) for data in f.readlines()]

    operator_groups = {"PART 1": "+*", "PART 2": "+* "}  # " " is concatenation operator
    for part, op_group in operator_groups.items():
        print(f"{part}: {get_total_calib(op_group)}")
