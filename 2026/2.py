from functools import reduce
import sys

def subsequences(s: str, size: int) ->list[str]:
    seqs = list()
    buf = list()

    for c in s:
        buf.append(c)
        if (len(buf) == size):
            seqs.append("".join(buf))
            buf = list()
    if buf:
        seqs.append("".join(buf))
    return seqs

# 2b
def is_invalid_fractal(i: int) -> bool:
    s = str(i)
    l = len(s)

    for ind in range(1, int(len(s) / 2) + 1):
        subseqs = subsequences(s, ind)
        last_seq = subseqs[0]
        seen_diff = False

        for seq in subseqs:
            if last_seq != seq:
                seen_diff = True
                break
            last_seq = seq
        
        if not seen_diff:
            return True

    return False

# 2a
def is_invalid(i: int) -> bool:
    s = str(i)
    pivot = int(len(s) / 2)
    return s[0:pivot] == s[pivot:]

def sum_range(l: list[int]) -> int:
    return reduce(lambda acc, val: acc + (val if is_invalid_fractal(val) else 0), l, 0)

def parse_range(s: str):
    first, last = s.split("-")
    return list(range(int(first), int(last) + 1))

acc = 0
for line in sys.stdin:
    ranges = line.split(",")
    for rng in ranges:
        acc += sum_range(parse_range(rng))
print(acc)