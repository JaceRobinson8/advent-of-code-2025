from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Bank:
    batteries: list[int]

    @classmethod
    def from_str(cls, batteries: str) -> Bank:
        return cls([int(x) for x in batteries])


def get_bank_joltage_p1(bank: Bank) -> int:
    # First get max value.
    # Then get max value to right of previous max
    # This produces the largest joltage
    # Corner case, first max can't be last digit
    max_index, max_val = max(enumerate(bank.batteries[:-1]), key=lambda x: x[1])
    max2_index, max2_val = max(
        enumerate(bank.batteries[(max_index + 1) :]), key=lambda x: x[1]
    )
    return int(str(max_val) + str(max2_val))


def get_bank_joltage_p2(bank: Bank, batteries_to_turn_on: int) -> int:
    batteries = []
    max_idx = -1
    total_batteries = len(bank.batteries)
    for idx in range(batteries_to_turn_on):
        max_idx, max_val = get_max_battery_in_slice(
            bank.batteries,
            range_start=max_idx + 1,
            range_end=total_batteries - batteries_to_turn_on + idx + 1,
        )
        batteries.append(str(max_val))
    return int("".join(batteries))


def get_max_battery_in_slice(
    batteries: list[int], range_start: int, range_end: int
) -> tuple[int, int]:
    return max(
        enumerate(batteries[range_start:range_end]),
        key=lambda x: x[1],
    )


def parse_file(file_path: str | Path) -> list[Bank]:
    file_path = Path(file_path)
    with open(file=file_path, mode="r") as f:
        return [Bank.from_str(line.strip()) for line in f]


def main():
    BASE_DIR = Path(__file__).resolve().parent
    banks = parse_file(BASE_DIR / "input_sample.txt")
    print(f"Answer (p1): {sum([get_bank_joltage_p1(bank) for bank in banks])}")
    print(f"Answer (p2): {sum([get_bank_joltage_p2(bank, 12) for bank in banks])}")


if __name__ == "__main__":
    main()
