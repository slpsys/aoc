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

class BatteryBank2():
    def __init__(self, size=12):
        self.max_joltage = ""
        self.size = size

    def add_battery(self, joltage: int):
        if len(self.max_joltage) == self.size:
            self._evaluate_for_add(joltage)
        else:
            self.max_joltage += str(joltage)

    def _evaluate_for_add(self, joltage: int):
        max = int(self.max_joltage)
        for i in range(len(self.max_joltage)):
            cnd = int(self.max_joltage[:i] + self.max_joltage[i + 1:] + str(joltage))
            if cnd > max:
                max = cnd
        self.max_joltage = str(max)

    def joltage(self) -> int:
        return int(self.max_joltage)

    def __str__(self) -> str:
        return str(self.max_joltage)
    
def parse_line(line: str) -> BatteryBank:
    bank = BatteryBank()
    for c in line:
        bank.add_battery(int(c))
    return bank

def parse_line2(line: str) -> BatteryBank2:
    bank = BatteryBank2()
    for c in line:
        bank.add_battery(int(c))
    return bank

acc = 0
acc_str = ""
for line in sys.stdin:
    ls = line.rstrip()
    b = parse_line2(ls)
    j = b.joltage()

    acc += j
    acc_str += f"{j} "

print(acc)
#print(acc_str)