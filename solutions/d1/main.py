from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class instruction:
    direction: str
    value: int


def read_file(file_path: str | Path) -> list[str]:
    with open(file=file_path, mode="r") as f:
        return f.readlines()


def count_0s(instructions: list[instruction]) -> int:
    dial = 50
    zero_count = 0
    for instr in instructions:
        dial += instr.value if instr.direction == "R" else instr.value * -1
        dial %= 100
        if dial == 0:
            zero_count += 1
    return zero_count


def p1():
    instructions = [
        instruction(direction=row[0], value=int(row[1:-1]))
        for row in read_file(BASE_DIR / "input1.txt")
    ]
    print(f"Answer: {count_0s(instructions=instructions)}")


if __name__ == "__main__":
    p1()
