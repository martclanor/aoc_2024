from dataclasses import dataclass


@dataclass(frozen=True)
class Con:
    in1: str
    in2: str
    op: str
    out: str

    @classmethod
    def from_data(cls, data):
        in1, op, in2, _, out = data.split()
        return cls(in1, in2, op, out)

    def solve(self):
        if self.op == "OR":
            return inputs[self.in1] or inputs[self.in2]
        if self.op == "AND":
            return inputs[self.in1] and inputs[self.in2]
        if self.op == "XOR":
            return inputs[self.in1] ^ inputs[self.in2]
        return None


if __name__ == "__main__":
    with open("day_24/input.txt") as f:
        _i, _c = f.read().strip().split("\n\n")

    inputs = {k: bool(int(v)) for k, v in (i.split(": ") for i in _i.split("\n"))}
    cons = set(Con.from_data(c) for c in _c.split("\n"))
    cons2 = cons.copy()  # Keep a copy to iterate on while modifying cons

    # Remove each item in cons while adding to inputs
    while cons:
        for con in cons2:
            if con.in1 in inputs and con.in2 in inputs:
                if con.out in inputs and con in cons:
                    cons.remove(con)
                else:
                    inputs[con.out] = con.solve()

    decimal = []
    for i in sorted(inputs, reverse=True):
        if i[0] != "z":
            continue
        decimal.append(str(int(inputs[i])))
    print(f"PART 1: {int("".join(decimal), 2)}")
