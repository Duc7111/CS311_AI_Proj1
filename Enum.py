
from enum import Enum

class BlockState(Enum):
    EMPTY = '0'
    WALL = '-1' 
    UP = 'UP'
    DOWN = 'DO'
    AGENT = 'A'
    TASK = 'T'
    KEY = 'K'
    DOOR = 'D'

class MSG(Enum):
    MOVEABLE = 'MOVABLE'
    BLOCKED = 'BLOCKED'
    UP = 'UP'
    DOWN = 'DOWN'
    KEY = 'KEY'