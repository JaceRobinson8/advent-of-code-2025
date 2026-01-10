from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from itertools import batched


@dataclass(frozen=True)
class IDRange:
    start: int  # inclusive on start
    end: int  # inclusive on end

    @classmethod
    def from_str(cls, raw_range: str) -> IDRange:
        range_pair = raw_range.split("-")
        return cls(start=int(range_pair[0]), end=int(range_pair[1]))


def parse_file(file_path: str | Path) -> list[IDRange]:
    file_path = Path(file_path)
    with open(file=file_path, mode="r") as f:
        data_line = f.readline()
        return [
            IDRange.from_str(raw_range.strip()) for raw_range in data_line.split(",")
        ]


def get_invalid_idx_from_ranges(
    idx_ranges: list[IDRange], num_repeats: int = -1
) -> list[int]:
    result: list[int] = []
    for idx_range in idx_ranges:
        result.extend(get_invalid_idx_from_range(idx_range, num_repeats))
    return result


def get_invalid_idx_from_range(idx_range: IDRange, num_repeats: int = -1) -> list[int]:
    return [
        idx
        for idx in range(idx_range.start, idx_range.end + 1)
        if is_invalid_id(str(idx), num_repeats)
    ]


def is_invalid_id(idx: str, num_repeats: int = -1) -> bool:
    """num_repeats = -1 check for repeat at least twice.

    Otherwise check exactly num_repeats.
    """
    invalid = False
    if num_repeats == -1:  # no length specified, try every combination
        for i in range(len(idx) - 1):
            if len(set(batched(idx, i + 1))) == 1:
                invalid = True
                break
    else:
        batch_size = max(int(len(idx) / num_repeats), 2)
        invalid = len(set(batched(idx, batch_size))) == 1
    return invalid


def main():
    BASE_DIR = Path(__file__).resolve().parent
    idx_ranges = parse_file(BASE_DIR / "input1.txt")
    print(f"Answer (p1): {sum(get_invalid_idx_from_ranges(idx_ranges, 2))}")
    print(f"Answer (p2): {sum(get_invalid_idx_from_ranges(idx_ranges, -1))}")


if __name__ == "__main__":
    main()
