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

def get_input_type(line: str) -> InputType:
    if re.match(r'\d+-\d+$', line):
        return InputType.FRESH_ITEM_RANGE
    elif re.match(r'\d+$', line):
        return InputType.AVAILABLE_ITEM
    elif re.match(r'\s*$', line):
        return InputType.SEPARATOR
    else:
        return InputType.INVALID

def parse_item_range(rng: str) -> range[int]:
    frm, t = rng.split("-", 1)
    return range(int(frm), int(t) + 1)

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
