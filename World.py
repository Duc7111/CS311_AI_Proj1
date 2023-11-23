
from Enum import BlockState as bs, MSG as msg

from Map import Map
from Entity import Entity, Agent, Key

class World:
    floors = [] # maps
    agents = {} # agentID (int): floor (Map)
    keys = {}

    def __init__(self, string: str):

        pass

    def __str__(self) -> str: # cast from map to string

        pass

    def __notEmpty(self, entity: Entity):
        
        pass

    def _check(self, n: int, m: int, id: int) -> str:
        agent = self.agents[id]
        n += agent.pos[1]
        m += agent.pos[2]
        if n not in range(0, self.n) or m not in range(0, self.m):
            return msg.BLOCKED.value
        base = self.floor[agent.pos[0]].base
        for a in self.agents:
            if a.pos == [agent.pos[0], n, m]:
                return msg.BLOCKED.value
        if base[n][m] == bs.WALL.value:
            return msg.BLOCKED.value
        elif base[n][m] == bs.UP.value:
            return msg.UP.value
        elif base[n][m] == bs.DOWN.value:
            return msg.DOWN.value
        elif base[n][m][0] == 'K':
            agent.keys[int(base[n][m].replace('K', ''))] = 1
            return msg.KEY.value
        elif base[n][m][0] == 'D':
            if int(base[n][m].replace('D', '')) in agent.keys:
                return msg.MOVEABLE.value
            else:
                return msg.BLOCKED.value
        else:
            return msg.MOVEABLE.value

    # movable -> move + return true | else return false
    # n, m: -1, 0, 1
    def move(self, n: int, m: int, agentID: int = 0) -> bool:
        match self._check(n, m, agentID):
            case msg.BLOCKED.value:
                return False
            case msg.MOVEABLE.value:
                self.agents[agentID].pos[1] += n
                self.agents[agentID].pos[2] += m
            case msg.UP.value:
                self.agents[agentID].pos[0] += 1
                self.agents[agentID].pos[1] += n
                self.agents[agentID].pos[2] += m
            case msg.DOWN.value:
                self.agents[agentID].pos[0] += -1
                self.agents[agentID].pos[1] += n
                self.agents[agentID].pos[2] += m
            case msg.KEY.value: # _check add key already
                self.agents[agentID].pos[1] += n
                self.agents[agentID].pos[2] += m
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
        

