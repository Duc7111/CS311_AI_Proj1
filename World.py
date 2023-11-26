
from Enum import BlockState as bs, MSG as msg

from Entity import Entity, Agent, Key
from Map import Map

class World:
    floors = [] # maps
    agents = {} # agentID, agent
    keys = {}

    def __init__(self, dir: str):
        file = open(dir, 'r')
        line = file.readline()
        sizes = line.split(',')
        sizes[0] = int(sizes[0])
        sizes[1] = int(sizes[1])
        line = file.readline() # read floor name. kinda skip it
        while line != '':
            map = Map(sizes[0], sizes[1])
            for i in range (0, sizes[0]):
                line = file.readline()
                cells = line.split(',')
                for j in range(0, sizes[1]):
                    map.base[i][j] = cells[j] if cells[j][0] != bs.AGENT.value else 0 # storing Agents seperately
            self.floors.append(map)
            line = file.readline() # read the next line indicate next floor name
        pass

    def __notEmpty(self, entity: Entity):
        
        pass

    def _check(self, n: int, m: int, id: int) -> str:
        agent = self.agents[id]
        n += agent.pos[1]
        m += agent.pos[2]
        if n not in range(0, self.n) or m not in range(0, self.m):
            return msg.BLOCKED.value
        base = self.floors[agent.pos[0]].base
        for a in self.agents:
            if a.pos == [agent.pos[0], n, m]:
                return msg.BLOCKED.value
        if base[n][m] == bs.WALL.value:
            return msg.BLOCKED.value
        elif base[n][m] == bs.UP.value:
            return msg.UP.value
        elif base[n][m] == bs.DOWN.value:
            return msg.DOWN.value
        elif base[n][m][0] == bs.KEY.value: # First char
            return msg.KEY.value
        elif base[n][m][0] == bs.DOOR.value:
            if base[n][m].replace('D', 'K') in agent.keys:
                return msg.MOVEABLE.value
            else:
                return msg.BLOCKED.value
        else:
            return msg.MOVEABLE.value

    # movable -> move + return true | else return false
    # n, m: -1, 0, 1
    def move(self, n: int, m: int, agentID: int = 0) -> bool:
        agent = self.agents[agentID]
        base = self.floors[agent.pos[0]].base
        if n != 0 and m != 0: # diagonal moves
            if self._check(0, m, agentID) == msg.BLOCKED.value or self._check(n, 0, agentID) == msg.BLOCKED.value:
                return False
        match self._check(n, m, agentID):
            case msg.BLOCKED.value:
                return False
            case msg.MOVEABLE.value:
                agent._move(n, m)
            case msg.UP.value:
                agent.pos[0] += 1
                agent._move(n, m)
            case msg.DOWN.value:
                agent.pos[0] += -1
                agent._move(n, m)
            case msg.KEY.value:
                agent._move(n, m)
                agent.keys[base[agent.pos[1]][agent.pos[2]]] = 1 # add key
        return True

    def addWall(self, entity: Entity) -> bool:
        if self.__notEmpty(entity):
            return False
        base = self.floors[entity.pos[0]]
        base[entity.pos[1]][entity.pos[2]] = bs.WALL.value
        return True
    
    def addAgent(self, agent: Agent, id: int) -> bool:
        if id in self.agents or self.__notEmpty(agent) or self.__notEmpty(agent):
            return False
        base = self.floors[agent.pos[0]]
        base[agent.pos[1]][agent.pos[2]] = bs.AGENT.value + str(id)
        base[agent.task[1]][agent.task[2]] = bs.TASK.value + str(id)
        return True
        
    def addKey(self, key: Key, id: int) -> bool:
        if id in self.keys or self.__notEmpty(key) or self.__notEmpty(key):
            return False
        self.keys[id] = key
        self.base[key.pos[0]][key.pos[1]] = bs.KEY.value + str(id) 
        self.base[key.door[0]][key.door[1]] = bs.DOOR.value + str(id) # Setup doors
        

