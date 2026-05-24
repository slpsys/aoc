import sys

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        print(f"({self.x}, {self.y})")

class BoundingBox:
    def __init__(self, nw: Point=None, se: Point=None):
        self.nw = nw if nw else Point(0, 0)
        self.se = se if se else Point(0, 0)
    
    def __str__(self) -> str:
        return f"({self.nw.x}, {self.nw.y}) - ({self.se.x}, {self.se.y})"

def safe_offset(p: Point, x_max, y_max, x_off=1, y_off=1) -> BoundingBox:
    b = BoundingBox()
    b.nw.x = (p.x - x_off) if (p.x - x_off > 0) else 0
    b.nw.y = (p.y - y_off) if (p.y - y_off > 0) else 0 
    b.se.x = (p.x + x_off) if (p.x + x_off < x_max) else x_max
    b.se.y = (p.y + y_off) if (p.y + y_off < y_max) else y_max
    return b

def assess_cell(rows: list[str], p: Point, box: BoundingBox, on_char: str) -> int:
    val = 0

    for ix in range(box.nw.x, box.se.x + 1):
        for iy in range(box.nw.y, box.se.y + 1):
            if p.x == ix and p.y == iy:
                continue

            if rows[iy][ix] == on_char:
                val += 1
    return val

def assess_rolls(rows: list[str], on_char: str = "@") -> int:
    # Assume rectangular
    height = len(rows)
    width = len(rows[0])
    accessible = []

    for row in range(height):
        for column in range(width):
            p = Point(column, row)
            if rows[row][column] != on_char:
                continue

            bounding_box = safe_offset(p, width - 1, height - 1)
            score = assess_cell(rows, p, bounding_box, on_char)
            if score < 4:
                accessible.append(p)
    return accessible

def replace_rolls(rows: list[str], rolls: list[Point], replacement_char: str="."):
    for r in rolls:
        rows[r.y] = rows[r.y][0:r.x] + replacement_char + rows[r.y][r.x + 1:]

grid_rows = []
for line in sys.stdin:
    ls = line.rstrip()
    grid_rows.append(ls)

removed = 0
while True:
    accessible_rolls = assess_rolls(grid_rows)
    
    if len(accessible_rolls) == 0:
        break

    removed += len(accessible_rolls)
    replace_rolls(grid_rows, accessible_rolls)

print(removed)