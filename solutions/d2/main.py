from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass


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


def get_invalid_idx_from_ranges(idx_ranges: list[IDRange]) -> list[int]:
    result: list[int] = []
    for idx_range in idx_ranges:
        result.extend(get_invalid_idx_from_range(idx_range))
    return result


def get_invalid_idx_from_range(idx_range: IDRange) -> list[int]:
    return [
        idx
        for idx in range(idx_range.start, idx_range.end + 1)
        if is_invalid_id(str(idx))
    ]


def is_invalid_id(idx: str) -> bool:
    # Invalid id repeats a sequence
    id_length = len(idx)

    if (len(idx) % 2) == 1:  # odd length sequences won't be invalid
        return False
    else:
        return idx[: int(id_length / 2)] == idx[int(id_length / 2) :]


def main():
    BASE_DIR = Path(__file__).resolve().parent
    idx_ranges = parse_file(BASE_DIR / "input1.txt")
    print(f"Answer (p1): {sum(get_invalid_idx_from_ranges(idx_ranges))}")

    # print(f"Answer (p2): {count_0s_p2(rotations=rotations)}")


if __name__ == "__main__":
    main()
