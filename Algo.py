from World import World
from queue import PriorityQueue
from Node import Node
import copy

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

def bfs(world):
    agent = world.agents["A1"]

    queue = [Node(agents = agent)]
    visited = set()
    visited.add(tuple(agent.pos))

    while queue:
        current = queue.pop(0)
        agentCurrent = current.agents
        if current.isGoal() == True:
            return current

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.append(Node(parent = current, agents = agentNext))
                visited.add(tuple(agentNext.pos))

    return None


def UCS(world):
    agent = world.agents["A1"]

    queue = PriorityQueue()
    queue.put(Node(agents = agent))
    visited = set()

    while queue:
        current = queue.get()
        agentCurrent = current.agents
        visited.add(tuple(agentCurrent.pos))

        if current.isGoal() == True:
            return current

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.put(Node(parent = current, agents = agentNext, g = current.g + 1))

    return None

def Astar(world):
    agent = world.agents["A1"]

    queue = PriorityQueue()
    queue.put(Node(agents = agent))
    visited = set()

    while queue:
        current = queue.get()
        agentCurrent = current.agents
        visited.add(tuple(agentCurrent.pos))

        if current.isGoal() == True:
            return current

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.put(Node(parent = current, agents = agentNext, g = current.g + 1, h = agentNext.MED()))

    return None