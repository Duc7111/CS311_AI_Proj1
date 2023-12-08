from typing import List

from Enum import BlockState as bs, MSG as msg

from Entity import Entity, Agent, Key
from Map import Map
from copy import deepcopy

class World:
    floors = [] # maps
    agents = {} # agentID, agent
    keys = {} # keyID, key
    n = 0 # row
    m = 0 # col

    def __init__(self, dir: str):
        file = open(dir, 'r')
        line = file.readline()
        sizes = line.split(',')
        self.n = int(sizes[0])
        self.m = int(sizes[1])
        line = file.readline() # read floor name. kinda skip it
        f = 0
        while line != '':
            if line == '\n':
                line = file.readline()
                continue
            map = Map(self.n, self.m)
            for i in range (0, self.n):
                line = file.readline().replace('\n', '')
                cells = line.split(',')
                for j in range(0, self.m):
                    map.base[i][j] = cells[j] if cells[j][0] != bs.AGENT.value else '0' 
                    # storing Agents seperately
                    if cells[j][0] == bs.AGENT.value:
                        if cells[j] not in self.agents:
                            self.agents[cells[j]] = Agent(f, i, j)
                        else:
                            self.agents[cells[j]].pos = [f, i, j]
                    # store task in agent
                    if cells[j][0] == bs.TASK.value:
                        agentID = cells[j].replace(bs.TASK.value, bs.AGENT.value)
                        # create temp agent if not exist
                        if agentID not in self.agents:
                            self.agents[agentID] = Agent(f, i, j)
                        self.agents[agentID].task = Entity(f, i, j)
                    # store random access key
                    elif cells[j][0] == bs.KEY.value:
                        if cells[j] not in self.keys:
                            key = Key(f, i, j)
                            self.keys[cells[j]] = key
                        else:
                            self.keys[cells[j]].pos = [f, i, j]
                    # store doors in key
                    elif cells[j][0] == bs.DOOR.value:
                        keyID = cells[j].replace(bs.DOOR.value, bs.KEY.value)
                        # create temp key if not exist
                        if keyID not in self.keys:
                            self.keys[keyID] = Key(f, i, j)
                        self.keys[keyID].doors.append(Entity(f, i, j))
            self.floors.append(map)
            f += 1
            line = file.readline() # read the next line indicate next floor name
        pass

    def _check(self, n: int, m: int, agent: Agent) -> str:
        x = n + agent.pos[1]
        y = m + agent.pos[2]
        if x not in range(0, self.n) or y not in range(0, self.m):
            return msg.BLOCKED.value
        base = self.floors[agent.pos[0]].base
        for a in self.agents.values():
            if a.pos == [agent.pos[0], x, y]:
                return msg.BLOCKED.value
        if base[x][y] == bs.WALL.value:
            return msg.BLOCKED.value
        elif base[x][y] == bs.UP.value:
            return msg.UP.value
        elif base[x][y] == bs.DOWN.value:
            return msg.DOWN.value
        elif base[x][y][0] == bs.KEY.value: # First char
            return msg.KEY.value
        elif base[x][y][0] == bs.DOOR.value:
            if base[x][y].replace('D', 'K') in agent.keys:
                return msg.MOVEABLE.value
            else:
                return msg.BLOCKED.value
        else:
            return msg.MOVEABLE.value

    # movable -> move + return true | else return false
    # n, m: -1, 0, 1
    def move(self, n: int, m: int, agent: Agent) -> bool:
        base = self.floors[agent.pos[0]].base
        if n != 0 and m != 0: # diagonal moves
            if self._check(0, m, agent) == msg.BLOCKED.value or self._check(n, 0, agent) == msg.BLOCKED.value:
                return False
        match self._check(n, m, agent):
            case msg.BLOCKED.value:
                return False
            case msg.MOVEABLE.value:
                agent._move(n, m)
            case msg.UP.value:
                agent.pos[0] += 1
                agent._move(n, m)
            case msg.DOWN.value:
                agent.pos[0] += -1
            case msg.KEY.value:
                agent._move(n, m)
                agent.keys[base[agent.pos[1]][agent.pos[2]]] = 1 # add key
        return True

    def getToDoList(self, agent: Agent) -> []:
        keys = [key for key in agent.keys] 
        main = self.floors[agent.task.pos[0]].scan(keys, agent.task)
        spanKeys = {}
        for door in main[0]:
            keyID = door[1].replace(bs.DOOR.value, bs.KEY.value)
            if keyID not in spanKeys:
                tempAgent = Agent(agent.pos[0], agent.pos[1], agent.pos[2])
                tempAgent.keys = keys
                tempAgent.task = self.keys[keyID]               
                spanKeys[keyID] = self.getToDoList(tempAgent)

    def get_floor_array(self, floor_index: int) -> List[List[str]]:

        if 0 <= floor_index < len(self.floors):
            return self.floors[floor_index].base
        else:
            # Handle invalid floor index (you can raise an exception or return a default value)
            return []