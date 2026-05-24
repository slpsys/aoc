from enum import StrEnum, auto
from functools import reduce
import sys

class ManifoldCharacters(StrEnum):
    SPACE = '.'
    TACHYON_START = 'S'
    SPLITTER = '^'
    TACHYON_BEAM = '|'
    UNKNOWN = auto()


class Manifold:
    def __init__(self):
        self.manifold_lines = []
        self.width = 0
        self.split = 0

    def load_manifold_line(self, s: str):
        if not self.manifold_lines:
            self.width = len(s)
        self.manifold_lines.append(s)
        self._evaluate_and_update_line(len(self.manifold_lines) - 1)

    def _swap_char(s: str, ix: int, sw: str) -> str:
        return s[0:ix] + sw + s[ix + 1:]

    def _evaluate_and_update_line(self, i: int):
        if i == 0:
            print(self.manifold_lines[i])
            return

        skip_next = False
        for ix in range(self.width):
            if skip_next:
                skip_next = False
                continue

            lc = self.manifold_lines[i][ix]
            pc = self.manifold_lines[i-1][ix]
            current = ManifoldCharacters(lc)
            previous = ManifoldCharacters(pc)

            match previous:
                case ManifoldCharacters.TACHYON_START:
                    if current == ManifoldCharacters.SPACE:
                        self.manifold_lines[i] = Manifold._swap_char(self.manifold_lines[i], ix, str(ManifoldCharacters.TACHYON_BEAM))
                case ManifoldCharacters.TACHYON_BEAM:
                    if current == ManifoldCharacters.SPACE:
                        self.manifold_lines[i] = Manifold._swap_char(self.manifold_lines[i], ix, str(ManifoldCharacters.TACHYON_BEAM))
                    elif current == ManifoldCharacters.SPLITTER:
                        self.split += 1
                        if ix > 0:
                            self.manifold_lines[i] = Manifold._swap_char(self.manifold_lines[i], ix - 1, str(ManifoldCharacters.TACHYON_BEAM))
                        if ix < (self.width - 1):
                            self.manifold_lines[i] = Manifold._swap_char(self.manifold_lines[i], ix + 1, str(ManifoldCharacters.TACHYON_BEAM))
        print(self.manifold_lines[i])

    def count_splits(self) -> int:
        return self.split

m = Manifold()
for line in sys.stdin:
    ls = line.rstrip("\n")
    m.load_manifold_line(ls)
    
print(m.count_splits())
