from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Bank:
    batteries: list[int]

    @classmethod
    def from_str(cls, batteries: str) -> Bank:
        return cls([int(x) for x in batteries])


def get_bank_joltage(bank: Bank, batteries_to_turn_on: int) -> int:
    active_battery_joltage: list = []
    max_idx: int = -1
    total_batteries = len(bank.batteries)
    for idx in range(batteries_to_turn_on):
        max_idx, max_val = get_max_battery_in_slice(
            bank.batteries,
            start=max_idx + 1,
            end=total_batteries - batteries_to_turn_on + 1 + idx,
        )
        active_battery_joltage.append(str(max_val))
    return int("".join(active_battery_joltage))


def get_max_battery_in_slice(
    batteries: list[int], start: int, end: int
) -> tuple[int, int]:
    max_idx, max_val = max(
        enumerate(batteries[start:end]),
        key=lambda x: x[1],
    )
    return max_idx + start, max_val


def parse_file(file_path: str | Path) -> list[Bank]:
    file_path = Path(file_path)
    with open(file=file_path, mode="r") as f:
        return [Bank.from_str(line.strip()) for line in f]


def main():
    BASE_DIR = Path(__file__).resolve().parent
    banks = parse_file(BASE_DIR / "input1.txt")
    print(f"Answer (p1): {sum([get_bank_joltage(bank, 2) for bank in banks])}")
    print(f"Answer (p2): {sum([get_bank_joltage(bank, 12) for bank in banks])}")


if __name__ == "__main__":
    main()
