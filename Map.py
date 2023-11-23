
from io import TextIOWrapper

from Enum import BlockState as bs


class Map:
    n = 0
    m = 0
    base = []

    def __init__(self, n: int, m: int) -> None:
        self.base = [[bs.EMPTY.value for _ in m] for _ in n]
        self.n = n
        self.m = m

    def _notEmpty(self, pos: list):
        return self.base[pos[0]][pos[1]] != bs.EMPTY.value
    
    def _read(fin: TextIOWrapper) -> None:
        pass

    def _write(fout: TextIOWrapper) -> None:
        pass

    