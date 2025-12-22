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
    #print(f"Evaluating ({x}, {y}): {box}, {val}. {list(range(box.nw_x, box.se_x))} x {list(range(box.nw_y, box.se_y))}")

    return val

def assess_rolls(rows: list[str], on_char: str = "@") -> int:
    # Assme rectangular
    height = len(rows)
    width = len(rows[0])
    accessible = []

    for row in range(height):
        for column in range(width):
            if rows[row][column] != on_char:
                continue

            bounding_box = safe_offset(Point(column, row), width - 1, height - 1)
            score = assess_cell(rows, Point(column, row), bounding_box, on_char)
            if score < 4:
                accessible.append(Point(column, row))
    return accessible

grid_rows = []
for line in sys.stdin:
    ls = line.rstrip()
    grid_rows.append(ls)

accessible_rolls = assess_rolls(grid_rows)
print(len(accessible_rolls))
