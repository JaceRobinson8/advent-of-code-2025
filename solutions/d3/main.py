from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Bank:
    batteries: list[int]

    @classmethod
    def from_str(cls, batteries: str) -> Bank:
        return cls([int(x) for x in batteries])


def get_bank_joltage_rearrange(bank: Bank) -> int:
    # I misread the problem, in this solution you can rearrange batteries
    (
        max_index,
        max_val,
    ) = max(enumerate(bank.batteries), key=lambda x: x[1])
    bank.batteries.remove(max_val)
    # Second largest values
    (
        max2_index,
        max2_val,
    ) = max(enumerate(bank.batteries), key=lambda x: x[1])
    if max_index <= max2_index:
        bank_joltage = int(str(max_val) + str(max2_val))
    else:
        bank_joltage = int(str(max2_val) + str(max_val))
    return bank_joltage


def get_bank_joltage(bank: Bank) -> int:
    # First get max value.
    # Then get max value to right of previous max
    # This produces the largest joltage
    # Corner case, first max can't be last digit
    max_index, max_val = max(enumerate(bank.batteries[:-1]), key=lambda x: x[1])
    max2_index, max2_val = max(
        enumerate(bank.batteries[(max_index + 1) :]), key=lambda x: x[1]
    )
    return int(str(max_val) + str(max2_val))


def parse_file(file_path: str | Path) -> list[Bank]:
    file_path = Path(file_path)
    with open(file=file_path, mode="r") as f:
        return [Bank.from_str(line.strip()) for line in f]


def main():
    BASE_DIR = Path(__file__).resolve().parent
    banks = parse_file(BASE_DIR / "input1.txt")
    print(f"Answer (p1): {sum([get_bank_joltage(bank) for bank in banks])}")
    # print(f"Answer (p2): {sum(get_invalid_idx_from_ranges(idx_ranges, -1))}")


if __name__ == "__main__":
    main()
