
from copy import deepcopy

from World import World
from Algo import decisionSearch, pathReader

class Level4:

    def __init__(self, world: World) -> None:
        self.agents = deepcopy(world.agents)
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

    def __localheur(self, world: World, agentKey: str, max_depth: int) -> list:
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        for move in moves:
            pass
        pass

    def move(self) -> int:
        change = False
        for agentKey, path in self.agents.items:
            # move in path
            moved = self.__move(agentKey, path)
            change = moved or change
            if agentKey == 'A1' and not moved:
                # if A1 reach it task, return -1
                agent = self.world.agents['A1']
                if agent.pos == self.world.agents['A1'].task.pos:
                    return -1
                # dodge calculation

                for n in range(-1, 2):
                    for m in range(-1, 2):
                        pass
                base = self.world.floors[agent.pos[0]].base[agent.pos[1]][agent.pos[2]]
                continue