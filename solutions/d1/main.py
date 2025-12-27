from __future__ import annotations
from pathlib import Path
from functools import reduce
from dataclasses import dataclass
import time


BASE_DIR = Path(__file__).resolve().parent
DIAL_MAX = 100


@dataclass(frozen=True)
class Rotation:
    value: int

    @classmethod
    def from_str(cls, rotation: str) -> Rotation:
        amount = int(rotation[1:])
        return cls(amount if rotation[0] == "R" else -amount)


@dataclass(frozen=False)
class ZeroCounter:
    dial: int
    zero_count: int


def parse_file(file_path: str | Path) -> list[Rotation]:
    file_path = Path(file_path)
    with open(file=file_path, mode="r") as f:
        return [Rotation.from_str(line.strip()) for line in f if line.strip()]


def apply_rotation(cur: ZeroCounter, rot: Rotation) -> ZeroCounter:
    new_dial = (cur.dial + rot.value) % DIAL_MAX  # apply rotation
    new_zero_count = cur.zero_count + (cur.dial == 0)  # count zeros
    return ZeroCounter(new_dial, new_zero_count)


# part 1
# Reduction solution
def count_0s_p1_reduction(rotations: list[Rotation], dial_start: int = 50) -> int:
    return reduce(apply_rotation, rotations, ZeroCounter(dial_start, 0)).zero_count


# part 1
# for loop
def count_0s_p1_loop(rotations: list[Rotation], dial_start: int = 50) -> int:
    # Initial state
    dial = dial_start
    zero_count = 0
    # Apply rotations, counting zeros
    for rot in rotations:
        dial = (dial + rot.value) % DIAL_MAX
        if dial == 0:  # zero found
            zero_count += 1
    return zero_count


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
    start = time.perf_counter()
    result = count_0s_p1_reduction(rotations=rotations)
    elapsed = time.perf_counter() - start
    print(f"Reduction sol time: {elapsed}")

    # For loop is faster and simplier!
    start = time.perf_counter()
    result = count_0s_p1_loop(rotations=rotations)
    elapsed = time.perf_counter() - start
    print(f"Loop sol time: {elapsed}")

    print(f"Answer (reduction): {count_0s_p1_reduction(rotations=rotations)}")
    print(f"Answer (loop): {count_0s_p1_loop(rotations=rotations)}")
    # print(f"Answer: {count_0s_p2(rotations=rotations)}")


if __name__ == "__main__":
    p1()
