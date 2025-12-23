from enum import Enum
from functools import reduce
import re
import sys

class InputType(Enum):
    INVALID = 0
    FRESH_ITEM_RANGE = 1
    AVAILABLE_ITEM = 2
    SEPARATOR = 3

class RecordRange():
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def is_in_range(self, i: int) -> bool:
        return i >= self.min and i <= self.max

    def conditional_merge(self, other_range: RecordRange) -> RecordRange:
        first = self if self.min <= other_range.min else other_range
        second = self if self.min > other_range.min else other_range

        if first.max < second.min:
            return None
        else:
            return RecordRange(first.min, max(first.max, second.max))

    def size(self) -> int:
        return self.max - self.min + 1
    
    def __str__(self):
        return f"RecordRange({self.min}, {self.max})"


def get_input_type(line: str) -> InputType:
    if re.match(r'\d+-\d+$', line):
        return InputType.FRESH_ITEM_RANGE
    elif re.match(r'\d+$', line):
        return InputType.AVAILABLE_ITEM
    elif re.match(r'\s*$', line):
        return InputType.SEPARATOR
    else:
        return InputType.INVALID

def parse_item_range_boundaries(rng: str) -> tuple[int, int]:
    frm, t = rng.split("-", 1)
    return (int(frm), int(t))

def parse_item_range(rng: str) -> range[int]:
    frm, t = parse_item_range_boundaries(rng)
    return range(frm, t + 1)

def part_a():
    fresh_items = []
    fresh_and_available = 0
    debug_records = 0
    for line in sys.stdin:
        ls = line.rstrip()
        type = get_input_type(ls)

        match type:
            case InputType.FRESH_ITEM_RANGE:
                frm, t = ls.split("-", 1)
                fresh_items.append(RecordRange(int(frm), int(t))) 
                debug_records += 1
                if debug_records % 1000 == 0:
                    print(f"Debug: {debug_records}")
            case InputType.AVAILABLE_ITEM:
                i = int(ls)
                if reduce(lambda acc, item: acc | True if item.is_in_range(i) else acc, fresh_items, False): 
                    fresh_and_available += 1

    print(fresh_and_available)


# Part B
fresh_ranges = []
for line in sys.stdin:
    ls = line.rstrip()
    type = get_input_type(ls)

    if type == InputType.FRESH_ITEM_RANGE:
        frm, t = parse_item_range_boundaries(ls)
        rng = RecordRange(frm, t)
        fresh_ranges.append(rng)

fresh_ranges.sort(key=lambda x: x.min)

i = 0
while i < len(fresh_ranges):
    rng = fresh_ranges[i]

    if i + 1 < len(fresh_ranges) and rng.conditional_merge(fresh_ranges[i + 1]):
        fresh_ranges[i] = rng.conditional_merge(fresh_ranges[i + 1])
        del fresh_ranges[i + 1]
    else:
        i += 1

print(reduce(lambda acc, x: acc + x.size(), fresh_ranges, 0))