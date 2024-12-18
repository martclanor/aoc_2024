def run(prog, rega, regb, regc):
    def get_combo(operand, rega, regb, regc):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return rega
            case 5:
                return regb
            case 6:
                return regc

    output = []
    pointer = 0

    while pointer < len(prog):
        opcode = prog[pointer]
        operand = prog[pointer + 1]
        combo = get_combo(operand, rega, regb, regc)
        match opcode:
            case 0:  # adv
                rega = rega // pow(2, combo)
            case 1:  # bxl
                regb = regb ^ operand
            case 2:  # bst
                regb = combo % 8
            case 3:  # jnz
                if rega != 0:
                    pointer = operand
                    continue
            case 4:  # bxc
                regb = regb ^ regc
            case 5:  # out
                output.append(str(combo % 8))
            case 6:  # bdv
                regb = rega // pow(2, combo)
            case 7:  # cdv
                regc = rega // pow(2, combo)
        pointer += 2

    return ",".join(output)


if __name__ == "__main__":
    with open("day_17/input.txt") as f:
        _regs, _prog = f.read().split("\n\n")
        rega, regb, regc = [int(reg.split(":")[1]) for reg in _regs.split("\n")]
        prog = [int(p) for p in _prog.split(":")[1].split(",")]

    print(f"PART 1: {run(prog, rega, regb, regc)}")
