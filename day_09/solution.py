from dataclasses import dataclass


@dataclass(slots=True)
class Data:
    index: int
    start: int
    end: int

    @property
    def size(self):
        return self.end - self.start + 1


class File(Data): ...


class Free(Data):
    def fits(self, other):
        if self.index > other.index:
            return False
        return self.size >= other.size


if __name__ == "__main__":
    with open("day_09/input.txt") as f:
        data = f.read().strip()

    # PART 1
    # Approach: Calculate checksum while compressing (not ideal)
    files = iter(data[::-2])
    frees = iter(data[1::2])
    jumplist = iter(data[::2])
    files_total = sum(map(int, data[::2]))

    free = int(next(frees))
    file = int(next(files))
    start = int(next(jumplist)) - 1
    value = len(data) // 2
    file_index = 0

    checksum = 0
    done = False
    while not done:
        next_file, next_free = False, False
        if free > file:
            free -= file
            diff = file
            file = int(next(files))
            next_file = True
        elif free < file:
            file -= free
            diff = free
            free = int(next(frees))
            next_free = True
        else:
            diff = file
            file = int(next(files))
            free = int(next(frees))
            next_file, next_free = True, True
        for _ in range(diff):
            start += 1
            if start == files_total:
                done = True
                break
            checksum += start * value
        if next_file:
            value -= 1
        if next_free:
            file_index += 1
            jump = int(next(jumplist))
            for _ in range(jump):
                start += 1
                if start == files_total:
                    done = True
                    break
                checksum += start * file_index
    print(f"PART 1: {checksum}")

    # PART 2
    # Approach: Parse, compress, calculate checksum
    # Parse data into File and Free
    start = 0
    files = []
    frees = []
    for i, char in enumerate(map(int, data)):
        if char == 0:
            continue
        if i % 2 == 0:
            files.append(File(i, start, start + char - 1))
        else:
            frees.append(Free(i, start, start + char - 1))
        start += char

    # Compress
    for i, file in enumerate(reversed(files), start=1):
        for free in frees:
            if free.fits(file):
                # If file fits in free, move file to free
                file_size, free_size = file.size, free.size
                file.start = free.start
                file.end = file.start + file_size - 1
                free.start = file.end + 1
                break

    # Calculate checksum
    checksum = 0
    for value, file in enumerate(files):
        for pos in range(file.size):
            checksum += (pos + file.start) * value
    print(f"PART 2: {checksum}")
