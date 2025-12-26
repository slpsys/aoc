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
    ADDITION = lambda acc, x: acc + int(x)
    MULTIPLICATION = lambda acc, x: acc * int(x)
    ADDITION_INITIAL = 0
    MULTIPLICATION_INITIAL = 1

    def __init__(self):
        self.vector = []
        self.operator = OperationType.INVALID
    
    def update_operand(self, index: int, s: str):
        if len(self.vector) == index:
            self.vector.append("")

        #if s != " ":
        self.vector[index] += s
    
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

def get_boundaries(lines: list[str]) -> list[int]:
    has_numeric = [False] * len(lines[0])
    for line in lines:
        for ci in range(len(line)):
            if line[ci].isnumeric():
                has_numeric[ci] = True

    boundaries = [0] 
    for index in range(len(has_numeric)):
        if not has_numeric[index]:
            boundaries.append(index)
    
    boundaries.append(len(lines[0]))
    return boundaries
        
v = []
boundaries = []
lines = []
for line in sys.stdin:
    ls = line.rstrip("\n")
    lines.append(ls)

boundaries = get_boundaries(lines)

for line in lines:
    for i in range(len(boundaries) - 1):
        token = line[boundaries[i]:(boundaries[i+1] + 1)]
        token = token[1:] if boundaries[i] > 0 else token
        token = token[:-1] if (boundaries[i+1] + 1) < len(line) else token
        
        if len(v) == i:
            v.append(VectorOperation())
        
        if token.strip().isnumeric():
            for ci in range(len(token)):
                v[i].update_operand(ci, token[ci])
        else:
            match token.strip():
                case "+":
                    op = OperationType.ADDITION
                case "*":
                    op = OperationType.MULTIPLICATION
                case _:
                    op = OperationType.INVALID
            v[i].set_operator(op)
      
print(reduce(lambda acc, x: acc + x.result(), v, 0))