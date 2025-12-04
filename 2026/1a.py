from abc import ABC, abstractmethod
from enum import Enum
import sys

class Direction(Enum):
    LEFT  = 0
    RIGHT = 1


class Dial(ABC):
    MAX = 100

    def __init__(self): 
        self.value  = 50
        self.zeroed = 0

    @classmethod
    @abstractmethod
    def rotate(self, amount: int, direction: Direction):
        pass

class OnZeroDial(Dial):
    def __init__(self):
        super().__init__()

    def rotate(self, amount: int, direction: Direction): 
        if direction == Direction.LEFT:
            self.value = (self.value - amount) % Dial.MAX
        else:
            self.value = (self.value + amount) % Dial.MAX
        if self.value == 0:
            self.zeroed += 1
        self

class ThroughZeroDial(Dial):
    def __init__(self):
        super().__init__()

    def rotate(self, amount: int, direction: Direction): 
        orig_value = self.value
        for i in range(amount):
            last_value = self.value
            if direction == Direction.LEFT:
                self.value = (self.value - 1) % Dial.MAX
                if self.value == 0:
                    self.zeroed += 1
            else:
                self.value = (self.value + 1) % Dial.MAX
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

d = ThroughZeroDial()
for line in sys.stdin:
    d.rotate(*parse_line(line.rstrip()))

print(d.zeroed)