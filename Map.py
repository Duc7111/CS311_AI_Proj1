
from copy import deepcopy

from Enum import BlockState as bs
from Entity import Entity


class Map:
    base = []

    def __init__(self, n: int, m: int) -> None:
        self.base = [[bs.EMPTY.value for _ in range(0, m)] for _ in range(0, n)]
        self.n = n
        self.m = m

    # return a list of undodgeable doors and a dict of spaned cells
    def scan(self, keys: [], task: Entity) -> []:
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1)) # down, up, right, left, skip diagnal moves
        frontier = [task]
        spaned = {task.pos: 0} # pos: cost
        doors = [] # pos, door, cost
        while len(frontier) != 0:
            span = frontier.pop(0)
            for move in moves:
                next = deepcopy(span)
                next.pos[1] += move[0]
                next.pos[2] += move[1]
                if next.pos[1] < 0 or next.pos[1] >= self.n or next.pos[2] < 0 or next.pos[2] >= self.m: 
                    continue
                if next.pos in spaned or self.base[next.pos[1]][next.pos[2]] in (bs.WALL.value, bs.UP.value, bs.DOWN.value):
                    continue
                if self.base[next.pos[1]][next.pos[2]][0] == bs.DOOR.value:
                    if self.base[next.pos[1]][next.pos[2]].replace(bs.DOOR.value, bs.KEY.value) not in keys:
                        doors.append((next, self.base[next.pos[1]][next.pos[2]], spaned[span.pos] + 1)) 
                        continue
                frontier.append(next)
                spaned[next.pos] = spaned[span.pos] + 1
        # remove dodgeable doors
        for door in doors:
            temp = deepcopy(door[0])
            for move in moves:
                temp.pos[1] += move[0]
                temp.pos[2] += move[1]
                if temp.pos[1] < 0 or temp.pos[1] >= self.n or temp.pos[2] < 0 or temp.pos[2] >= self.m:
                    temp.pos[1] -= move[0]
                    temp.pos[2] -= move[1]
                    continue
                if temp.pos in spaned:
                    doors.remove(door)
                    break
                temp.pos[1] -= move[0]
                temp.pos[2] -= move[1]
        return [doors, spaned]
    
    # continue scaning from the last scaned cell
    def reScan(self, spaned, doors, keys):
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1)) # down, up, right, left, skip diagnal moves
        frontier = [door for door in doors]
        while len(frontier) != 0:
            span = frontier.pop(0)
            for move in moves:
                next = deepcopy(span)
                next.pos[1] += move[0]
                next.pos[2] += move[1]
                if next.pos[1] < 0 or next.pos[1] >= self.n or next.pos[2] < 0 or next.pos[2] >= self.m: 
                    continue
                if next.pos in spaned or self.base[next.pos[1]][next.pos[2]] in (bs.WALL.value, bs.UP.value, bs.DOWN.value):
                    continue
                if self.base[next.pos[1]][next.pos[2]][0] == bs.DOOR.value:
                    if self.base[next.pos[1]][next.pos[2]].replace(bs.DOOR.value, bs.KEY.value) not in keys:
                        doors.append((next, self.base[next.pos[1]][next.pos[2]], spaned[span.pos] + 1))
                        continue
                frontier.append(next)
                spaned[next.pos] = spaned[span.pos] + 1
