import sys

class BoundingBox:
    def __init__(self, nw_x=0, nw_y=0, se_x=0, se_y=0):
        self.nw_x = nw_x
        self.nw_y = nw_y
        self.se_x = se_x
        self.se_y = se_y
    
    def __str__(self) -> str:
        return f"({self.nw_x}, {self.nw_y}) - ({self.se_x}, {self.se_y})"

def safe_offset(x, y, x_max, y_max, x_off=1, y_off=1) -> BoundingBox:
    b = BoundingBox()
    b.nw_x = (x - x_off) if (x - x_off > 0) else 0
    b.nw_y = (y - y_off) if (y - y_off > 0) else 0 
    b.se_x = (x + x_off) if (x + x_off < x_max) else x_max
    b.se_y = (y + y_off) if (y + y_off < y_max) else y_max
    return b

def assess_cell(rows: list[str], x: int, y: int, box: BoundingBox, on_char: str) -> int:
    val = 0

    for ix in range(box.nw_x, box.se_x + 1):
        for iy in range(box.nw_y, box.se_y + 1):
            if x == ix and y == iy:
                continue

            if rows[iy][ix] == on_char:
                val += 1
    #print(f"Evaluating ({x}, {y}): {box}, {val}. {list(range(box.nw_x, box.se_x))} x {list(range(box.nw_y, box.se_y))}")

    return val

def assess_rolls(rows: list[str], on_char: str = "@") -> int:
    # Assme rectangular
    height = len(rows)
    width = len(rows[0])
    accessible = 0

    debug_rows = []

    for row in range(height):
        debug_rows.append(rows[row])
        for column in range(width):
            if rows[row][column] != on_char:
                continue

            bounding_box = safe_offset(column, row, width - 1, height - 1)
            score = assess_cell(rows, column, row, bounding_box, on_char)
            if score < 4:
                accessible += 1
    return accessible

grid_rows = []
for line in sys.stdin:
    ls = line.rstrip()
    grid_rows.append(ls)

accessible_rolls = assess_rolls(grid_rows)
print(accessible_rolls)
