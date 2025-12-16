from functools import reduce
from heapq import *
import sys

class Battery():
    def __init__(self, joltage: int, order: int):
        self.joltage = joltage
        self.order   = order
    
    def joltage(self):
        return self.joltage
    
    def __lt__(self, other):
        return self.joltage < other.joltage

    def __le__(self, other):
        return self.joltage <= other.joltage

    def __gt__(self, other):
        return self.joltage > other.joltage

    def __ge__(self, other):
        return self.joltage >= other.joltage

    def __eq__(self, other):
        return self.joltage == other.joltage

    def __ne__(self, other):
        return self.joltage != other.joltage
    
    def __str__(self) -> str:
        return f"Joltage: {self.joltage}"
    
    

class BatteryBank():

    def __init__(self, *batteries: list[Battery]): 
        self.battery_heap = []

        if batteries:
            for b in batteries:
                self.add_battery(b)
    
    def add_battery(self, joltage: int):
        b = Battery(joltage, len(self.battery_heap))

        heappush_max(self.battery_heap, b)
    
    def batteries(self) -> list[Battery]:
        return self.batteries

    def joltage(self) -> int:
        max_heap = self.battery_heap.copy()
        top_battery = heappop_max(max_heap)
        right_battery = left_battery = None

        next_battery = heappop_max(max_heap)
        while next_battery:
            if next_battery.order < top_battery.order and not left_battery:
                left_battery = next_battery
            elif next_battery.order > top_battery.order and not right_battery:
                right_battery = next_battery
            next_battery = heappop_max(max_heap) if len(max_heap) else None
        
        left_joltage = (left_battery.joltage * 10) + top_battery.joltage if left_battery else 0
        right_joltage = (top_battery.joltage * 10) + right_battery.joltage if right_battery else 0

        # print(f"Bank: {self}\nLeft: {left_joltage}, Right: {right_joltage}")

        return left_joltage if left_joltage > right_joltage else right_joltage

    def __str__(self) -> str:
        battery_string = ",".join(map(lambda b: str(b), self.battery_heap))
        return f"Battery Bank: [{battery_string}]"
    
def parse_line(line: str) -> BatteryBank:
    bank = BatteryBank()
    for c in line:
        bank.add_battery(int(c))
    return bank

acc = 0
acc_str = ""
for line in sys.stdin:
    ls = line.rstrip()
    b = parse_line(ls)
    j = b.joltage()
    acc_str += str(j) + " "
    acc += j

print(acc)
print(acc_str)
    