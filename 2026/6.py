from enum import Enum
from functools import reduce
import re
import sys

class OperationType(Enum):
    INVALID = 0
    ADDITION = 1
    MULTIPLICATION = 2

class VectorOperation:
    INVALID = lambda acc, x: -1
    ADDITION = lambda acc, x: acc + x
    MULTIPLICATION = lambda acc, x: acc * x
    ADDITION_INITIAL = 0
    MULTIPLICATION_INITIAL = 1

    def __init__(self):
        self.vector = []
        self.operator = OperationType.INVALID
    
    def add_operand(self, i: int):
        self.vector.append(i)
    
    def set_operator(self, op: OperationType):
        self.operator = op

    def result(self) -> int:
        match self.operator:
            case OperationType.ADDITION:
                op = VectorOperation.ADDITION
                initial = VectorOperation.ADDITION_INITIAL
            case OperationType.MULTIPLICATION:
                op = VectorOperation.MULTIPLICATION
                initial = VectorOperation.MULTIPLICATION_INITIAL
            case _:
                op = VectorOperation.INVALID
                initial = -1
        return reduce(op, self.vector, initial)

    def __str__(self):
        return ", ".join(map(lambda x: str(x), self.vector)) + f" {str(self.operator)}"

def _process_token(bufs: str, v: list[VectorOperation], token_index: int):
    if bufs.isnumeric():
        if len(v) == token_index:
            v.append(VectorOperation())
        v[token_index].add_operand(int(bufs))
    elif bufs == "+":
        v[token_index].set_operator(OperationType.ADDITION)
    elif bufs == "*":
        v[token_index].set_operator(OperationType.MULTIPLICATION)
        
def parse_line(s: str, v: list[VectorOperation]):
    bufs = ""
    token_index = 0
    for i in range(len(s)):
        if s[i] == " " and len(bufs) > 0:
            _process_token(bufs, v, token_index)
            bufs = ""
            token_index += 1
        elif s[i].isnumeric() or s[i] == "+" or s[i] == "*":
            bufs += s[i]

    if (len(bufs) > 0):
        _process_token(bufs, v, token_index)
        
# Part B
v = []
for line in sys.stdin:
    ls = line.rstrip()
    parse_line(ls, v)

print(reduce(lambda acc, x: acc + x.result(), v, 0))
