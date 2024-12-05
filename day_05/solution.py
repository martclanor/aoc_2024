if __name__ == "__main__":
    with open("day_05/input.txt") as f:
        _checks, _updates = [
            line.split("\n") for line in f.read().rstrip("\n").split("\n\n")
        ]

    # Preprocess input
    checks = [tuple(map(int, c.split("|"))) for c in _checks]
    updates = [list(map(int, u.split(","))) for u in _updates]

    # PART 1
    total = 0
    for update in updates:
        for check in checks:
            if not (check[0] in update and check[1] in update):
                continue
            if update.index(check[0]) > update.index(check[1]):
                break
        else:
            total += update[len(update) // 2]
    print(f"PART 1: {total}")

    # PART 2
    total = 0
    for update in updates:
        modified = False
        while True:
            for check in checks:
                if not (check[0] in update and check[1] in update):
                    continue
                # Sort order is correct, skip check
                if (i := update.index(check[0])) < (j := update.index(check[1])):
                    continue
                # Sort order is NOT correct, swap elements, and repeat all checks
                else:
                    update[i], update[j] = update[j], update[i]
                    modified = True
                    break
            # Sort order is either just correct or corrected after modification
            else:
                if modified:
                    total += update[len(update) // 2]
                break
    print(f"PART 2: {total}")
