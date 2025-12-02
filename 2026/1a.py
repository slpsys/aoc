from enum import Enum
import sys

class Direction(Enum):
    LEFT  = 0
    RIGHT = 1

class Dial:
    MAX = 100

    def __init__(self):
        self.value  = 50
        self.zeroed = 0

    def rotate(self, amount: int, direction: Direction): 
        if direction == Direction.LEFT:
            self.value = (self.value - amount) % Dial.MAX
        else:
            self.value = (self.value + amount) % Dial.MAX
        if self.value == 0:
            self.zeroed += 1
        self
    
def parse_line(line: str):
    amount = 0
    direction = Direction.RIGHT

    if line[0] == "L":
        amount = int(line.removeprefix("L"))
        direction = Direction.LEFT
    else:
        amount = int(line.removeprefix("R"))

    return [amount, direction]

d = Dial()
for line in sys.stdin:
    d.rotate(*parse_line(line.rstrip()))

print(d.zeroed)