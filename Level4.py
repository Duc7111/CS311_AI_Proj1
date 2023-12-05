
import random
from copy import deepcopy

from Entity import Entity
from World import World
from Algo import decisionSearch, pathReader
from Enum import BlockState as bs

class Level4:

    def __init__(self, world: World) -> None:
        self.agents = deepcopy(world.agents) # agentKey: path, next
        self.world = world 
        self.__precompute()

    def __precompute(self) -> None:
        temp = self.agents
        # calculate level 3 solution for each agent
        for agentKey, agent in self.agents.items():
            self.world.agents = {agentKey: agent}
            path = pathReader(decisionSearch(self.world, agentKey))
            self.agents[agentKey] = [path, 1]
        # reset world
        self.world.agents = temp

    def __move(self, agentKey: str, path: list) -> bool:
        if path[1] < len(path[0]):
            cur = self.world.agents[agentKey].pos
            next = path[0][path[1]]
            if self.world.move(next[1] - cur[1], next[2] - cur[2], self.world.agents[agentKey]):
                path[1] += 1
                return True
        return False

    def move(self) -> int:
        change = False
        for agentKey, path in self.agents.items:
            agent = self.world.agents[agentKey]
            base = self.world.floors[agent.pos[0]].base[agent.pos[1]][agent.pos[2]]
            if path is None:
                # random a task
                self.agents[agentKey][0] = None
                while self.agents[agentKey][0] is None:
                    random.seed()
                    f = random.randint(0, len(self.world.floors) - 1)
                    n = random.randint(0, self.world.n - 1)
                    m = random.randint(0, self.world.m - 1)
                    if self.world.floors[f].base[n][m] == '0':
                        world = deepcopy(self.world)
                        world.agents = {agentKey: agent}
                        path = decisionSearch(world, agentKey)
                        if path is not None:
                            self.agents[agentKey][0] = pathReader(path)
                            self.agents[agentKey][1] = 1
                            agent.task = Entity(f, n, m)
            # move in path
            moved = self.__move(agentKey, path)
            change = moved or change
            if agentKey == 'A1' and not moved:
                # get blocking agent
                cur = agent.pos
                next = path[0][path[1]]
                if cur[1] == next[1] or cur[2] == cur[2]:
                    blockingKey = base[next[1]][next[2]]
                else:
                    blockingKeys = []
                    if base[next[1]][next[2]][0] == bs.AGENT.value:
                        blockingKeys.append(base[next[1]][next[2]])
                    if base[next[1]][cur[2]][0] == bs.AGENT.value:
                        blockingKeys.append(base[next[1]][cur[2]])
                    if base[cur[1]][next[2]][0] == bs.AGENT.value:
                        blockingKeys.append(base[cur[1]][next[2]])
            # check if agent has reached task    
            if agent.pos == agent.task.pos:
                self.agents[agentKey][0] = None
                agent.task = None
        return 0 if change else -2        
