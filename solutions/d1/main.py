from pathlib import Path
from dataclasses import dataclass
import math

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class instruction:
    direction: str
    value: int


def read_file(file_path: str | Path) -> list[str]:
    with open(file=file_path, mode="r") as f:
        return f.readlines()


# part 1
def count_0s_p1(instructions: list[instruction]) -> int:
    dial = 50
    zero_count = 0
    for instr in instructions:
        dial += instr.value if instr.direction == "R" else instr.value * -1
        dial %= 100
        if dial == 0:
            zero_count += 1
    return zero_count


# part 2
def count_0s_p2(instructions: list[instruction]) -> int:
    BASE = 100
    dial = 50
    zero_count = 0
    for instr in instructions:
        if dial == 0:  # special case if we start with 0
            dial += instr.value if instr.direction == "R" else instr.value * -1
            if (dial // BASE) < 0:
                zero_count += abs((dial // BASE)) - 1
            else:
                zero_count += abs((dial // BASE))
            dial %= BASE
            if dial == 0:
                zero_count += 1
        else:
            dial += instr.value if instr.direction == "R" else instr.value * -1
            # If dial is >= 0 or >=100, dial crossed 0
            if (dial // BASE) != 0:
                zero_count += abs((dial // BASE))
            if dial == 0:
                zero_count += 1
            dial %= BASE

    return zero_count


def p1():
    instructions = [
        instruction(direction=row[0], value=int(row[1:-1]))
        for row in read_file(BASE_DIR / "input_sample.txt")
    ]
    # print(f"Answer: {count_0s_p1(instructions=instructions)}")
    print(f"Answer: {count_0s_p2(instructions=instructions)}")


if __name__ == "__main__":
    p1()
