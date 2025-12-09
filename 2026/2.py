from functools import reduce
import sys

def is_invalid(i: int) -> bool:
    s = str(i)
    pivot = int(len(s) / 2)
    return s[0:pivot] == s[pivot:]

def sum_range(l: list[int]) -> int:
    return reduce(lambda acc, val: acc + (val if is_invalid(val) else 0), l, 0)

def parse_range(s: str):
    first, last = s.split("-")
    return list(range(int(first), int(last) + 1))

acc = 0
for line in sys.stdin:
    ranges = line.split(",")
    for rng in ranges:
        acc += sum_range(parse_range(rng))
print(acc)