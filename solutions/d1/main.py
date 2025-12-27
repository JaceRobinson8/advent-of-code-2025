from pathlib import Path
from functools import reduce
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent
DIAL_MAX = 100


class Rotation:
    value: int

    def __init__(self, rotation: str):
        amount = int(rotation[1:-1])
        self.value = amount if rotation[0] == "R" else -amount

    def __str__(self) -> str:
        self.value


@dataclass
class Result:
    dial: int
    zero_count: int


def parse_file(file_path: str | Path) -> list[Rotation]:
    with open(file=file_path, mode="r") as f:
        return [Rotation(row) for row in f.readlines()]


def apply_rotation(res: Result, rot: Rotation) -> Result:
    res.dial = (res.dial + rot.value) % DIAL_MAX  # apply rotation
    res.zero_count += 1 if res.dial == 0 else 0  # count zeros
    return res


# part 1
def count_0s_p1(rotations: list[Rotation], dial: int = 50) -> int:
    res = reduce(apply_rotation, rotations, Result(dial, 0))
    return res.zero_count


# part 2
def count_0s_p2(rotations: list[Rotation]) -> int:
    dial = 50
    zero_count = 0
    for instr in rotations:
        if dial == 0:  # special case if we start with 0
            dial += instr.value if instr.direction == "R" else instr.value * -1
            if (dial // DIAL_MAX) < 0:
                zero_count += abs((dial // DIAL_MAX)) - 1
            else:
                zero_count += abs((dial // DIAL_MAX))
            dial %= DIAL_MAX
            if dial == 0:
                zero_count += 1
        else:
            dial += instr.value if instr.direction == "R" else instr.value * -1
            # If dial is >= 0 or >=100, dial crossed 0
            if (dial // DIAL_MAX) != 0:
                zero_count += abs((dial // DIAL_MAX))
            if dial == 0:
                zero_count += 1
            dial %= DIAL_MAX

    return zero_count


def p1():
    rotations = parse_file(BASE_DIR / "input1.txt")
    print(f"Answer: {count_0s_p1(rotations=rotations)}")
    # print(f"Answer: {count_0s_p2(rotations=rotations)}")


if __name__ == "__main__":
    p1()
