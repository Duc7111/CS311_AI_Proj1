
from enum import Enum

from Entity import Agent, Key


class BlockState(Enum):
    EMPTY = '0'
    FULL = '-1'
    UP = 'UP'
    DOWN = 'DO'


class Map:
    n = 0
    m = 0
    base = []
    agents = []
    keys = []

    def __init__(self, n: int, m: int) -> None:
        self.base = [[BlockState.EMPTY for _ in m] for _ in n]
        self.n = n
        self.m = m
    
    def addEntity() -> bool:
        pass