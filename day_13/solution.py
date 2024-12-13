from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    button: str
    dx: int
    dy: int

    @classmethod
    def from_data(cls, data):
        return cls(
            button=data.partition(":")[0][-1],
            dx=int(data.partition("+")[2].partition(",")[0]),
            dy=int(data.partition("+")[2].partition("+")[-1]),
        )


@dataclass(frozen=True, slots=True)
class Position:
    x: int
    y: int

    @classmethod
    def from_data(cls, data):
        return cls(
            x=int(data.partition("=")[2].partition(",")[0]),
            y=int(data.partition("=")[2].partition("=")[-1]),
        )

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


@dataclass
class Combi:
    config_a: Config
    config_b: Config
    prize: Position

    def __post_init__(self):
        assert self.config_a.button == "A"
        assert self.config_b.button == "B"

    @classmethod
    def from_grouped_data(cls, data):
        return cls(*data)

    def get_nb(self):
        if na := self.get_na():
            nb = (self.prize.x - self.config_a.dx * na) / self.config_b.dx
            if nb.is_integer():
                return int(nb)
        return None

    def get_na(self):
        na = (self.config_b.dy * self.prize.x - self.config_b.dx * self.prize.y) / (
            self.config_b.dy * self.config_a.dx - self.config_b.dx * self.config_a.dy
        )
        if na.is_integer():
            return int(na)
        return None

    @property
    def cost(self):
        if (na := self.get_na()) and (nb := self.get_nb()):
            return 3 * na + nb
        return 0

    def correct_prize(self):
        self.prize = Position(self.prize.x, self.prize.y) + Position(
            10_000_000_000_000, 10_000_000_000_000
        )
        return self


@dataclass
class Tokens:
    na: int
    nb: int

    def __lt__(self, other):
        return self.cost < other.cost


if __name__ == "__main__":
    with open("day_13/input.txt") as f:
        combis = []
        for line in f.read().split("\n\n"):
            grouped_data = []
            for constructor, data in zip(
                (Config.from_data, Config.from_data, Position.from_data),
                line.split("\n"),
            ):
                grouped_data.append(constructor(data))
            combis.append(Combi.from_grouped_data(grouped_data))

    print(f"PART 1: {sum(combi.cost for combi in combis)}")
    print(f"PART 2: {sum(combi.correct_prize().cost for combi in combis)}")
