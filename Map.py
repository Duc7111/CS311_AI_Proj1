
from io import TextIOWrapper

from Enum import BlockState as bs


class Map:
    n = 0
    m = 0
    base = []

    def __init__(self, n: int, m: int) -> None:
        self.base = [[bs.EMPTY.value for _ in range(0, m)] for _ in range(0, n)]
        self.n = n
        self.m = m

    
    