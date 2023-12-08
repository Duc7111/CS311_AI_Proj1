
import random
from copy import deepcopy

from Entity import Entity
from World import World
from Algo import decisionSearch, pathReader
from Enum import BlockState as bs, MSG as msg

class Level4:

    def __init__(self, world: World) -> None:
        self.agents = deepcopy(world.agents) # agentKey: path, next
        self.world = world 
        self.blockLog = {}
        for agentKey in self.agents.keys():
            self.blockLog[agentKey] = []
        self.__precompute()

    def __precompute(self) -> None:
        temp = self.world.agents
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
         
    # return -1 if agent A1 has reached task, -2 if agent A1 has no possible move, 0 otherwise
    def move(self) -> int:
        change = False
        for agentKey, path in self.agents.items():
            agent = self.world.agents[agentKey]
            # move in path
            moved = self.__move(agentKey, path)
            change = moved or change
            if moved:
                self.blockLog[agentKey].clear()
            else:
                # get blocking agent
                cur = agent.pos
                next = path[0][path[1]]
                if cur[1] == next[1] or cur[2] == cur[2]:
                    for tempKey, temp in self.world.agents.items():
                        if  temp.pos == next:
                            self.blockLog[agentKey].append(tempKey)
                            break
                else:
                    for tempKey, temp in self.world.agents.items():
                        if temp.pos == next or temp.pos == [cur[0], next[1], cur[2]] or temp.pos == [cur[0], cur[1], next[2]]:
                            self.blockLog[agentKey].append(tempKey)
                # dodge calculation 
                if agentKey == 'A1':
                    # check if agent is in a deadlocked
                    deadlocked = False
                    blockTree = {}
                    frontier = self.blockLog[agentKey]
                    while len(frontier) > 0:
                        blockKey = frontier.pop(-1)
                        for tempKey in self.blockLog[blockKey]:
                            if tempKey not in blockTree.keys():
                                frontier.append(tempKey)
                                blockTree[tempKey] = None
                            else:
                                deadlocked = True
                                break
                        blockTree[blockKey] = 0

                    if deadlocked:
                        # if semi-deadlocked, dodge
                        if agentKey in blockTree.keys() and blockTree[agentKey] == 0:
                            # get movable cells
                            movable = {}
                            moves = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1))
                            for move in moves:
                                if self.world._check(move[0], move[1], agent) != msg.BLOCKED.value:
                                    movable[move] = 0
                            # count number of agents will get blocked by each move
                            for moves in movable:
                                pos = [agent.pos[0], agent.pos[1] + moves[0], agent.pos[2] + moves[1]]
                                for tempKey in self.agents:
                                    if tempKey == agentKey:
                                        continue
                                    tempPath = self.agents[tempKey]
                                    tempCur = tempPath[0][tempPath[1] - 1]
                                    tempNext = tempPath[0][tempPath[1]]
                                    if pos == tempNext:
                                        movable[move] += 1 if tempKey not in blockTree.keys() else 2 # prioritize semi-deadlock agents
                                    elif tempCur[1] != tempNext[1] and tempCur[2] != tempNext[2]:
                                        if pos == [tempCur[0], tempNext[1], tempCur[2]] or pos == [tempCur[0], tempCur[1], tempNext[2]]:
                                            movable[move] += 1 if tempKey not in blockTree.keys() else 2
                            # choose the move with least number of blocking agents
                            min = 100
                            m = None
                            for move in movable:
                                if movable[move] < min:
                                    min = movable[move]
                                    m = move
                            # move
                            if m is not None:
                                # add dodge move
                                path[0].insert(path[1], [agent.pos[0], agent.pos[1] + m[0], agent.pos[2] + m[1]])
                                # add return move
                                path[0].insert(path[1] + 1, [agent.pos[0], agent.pos[1], agent.pos[2]])
                                self.__move(agentKey, path)
                                change = True
                            # no possible move: quit
                            else:
                                return -2
                            continue

                        # else, find a new path
                        world = deepcopy(self.world)
                        path = decisionSearch(world, agentKey)
                        if path is not None:
                            self.agents[agentKey][0] = pathReader(path)
                            self.agents[agentKey][1] = 1
                            agent.task = Entity(path[0][1][0], path[0][1][1], path[0][1][2])
                            # dodge
                            path = self.agents[agentKey][0]
                            self.__move(agentKey, path)
                            change = True
                        # no path to dodge: quit
                        else:
                            return -2
                    # else, wait
            # check if agent has reached task    
            if agent.pos == agent.task.pos:
                if agentKey == 'A1':
                    return -1
                # random a task
                while agent.pos == agent.task.pos:
                    random.seed()
                    f = random.randint(0, len(self.world.floors) - 1)
                    n = random.randint(0, self.world.n - 1)
                    m = random.randint(0, self.world.m - 1)
                    if self.world.floors[f].base[n][m] == '0':
                        agent.task = Entity(f, n, m)
                        if agent.pos == agent.task.pos:
                            continue
                        world = deepcopy(self.world)
                        world.agents = {agentKey: agent}
                        path[0] = decisionSearch(world, agentKey)
                        path[0] = pathReader(path[0])
                        if path[0] is None:
                            continue
                        path[1] = 1
        return 0 if change else -2        

world = World('input3_level4.txt')
# init level 4
level4 = Level4(world)
# init paths
paths = {}
for agentKey, path in level4.agents.items():
    paths[agentKey] = [path[0][0]]
# move until all agents reach task
while True:
    result = level4.move()
    # record path
    for agentKey, path in level4.agents.items():
        if path[0] is not None:
            paths[agentKey].append(path[0][path[1] - 1])
            print(agentKey, path[0][path[1] - 1])
    if result == -1:
        print('A1 has reached task')
        break
    elif result == -2:
        print('No possible move')
        break

# print paths
for agentKey, path in paths.items():
    print(agentKey, path)
