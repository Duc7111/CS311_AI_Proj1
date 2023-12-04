from World import World
from queue import PriorityQueue
from Node import Node
from Entity import Agent
import copy

# direction to move
directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

# Level 1 algorithms
def bfs(world,update_screen_callback=None):
    agent = world.agents["A1"]

    queue = [Node(agents = agent)]
    visited = set()
    visited.add(tuple(agent.pos))
    steps = []  # Store the visited positions

    while queue:
        current = queue.pop(0)
        agentCurrent = current.agents
        steps.append(agentCurrent.pos)

        if current.isGoal() == True:
            return current, steps
        if update_screen_callback:
            update_screen_callback(world, agentCurrent.pos)
        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.append(Node(parent = current, agents = agentNext))
                visited.add(tuple(agentNext.pos))

    return None,steps


def UCS(world):
    agent = world.agents["A1"]

    queue = PriorityQueue()
    queue.put(Node(agents = agent))
    visited = set()

    while queue.empty() != True:
        current = queue.get()
        agentCurrent = current.agents

        if tuple(agentCurrent.pos) in visited:
            continue

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

    while queue.empty() != True:
        current = queue.get()
        agentCurrent = current.agents

        if tuple(agentCurrent.pos) in visited:
            continue

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

# Level 2 + 3:
def searchKey(currentState: Node, world: World):
    queue = [currentState]
    visited = set()
    visited.add(tuple(currentState.agents.pos))
    checkpointQueue = []
    # print("from:", agent.keys)
    while queue:
        current = queue.pop(0)
        agentCurrent = current.agents
        # print(agentCurrent.pos)
        if current.isGoal() == True:
            checkpointQueue.append(current)
            return checkpointQueue
        if agentCurrent.keys != currentState.agents.keys:
            # print(agentCurrent.pos)
            # print("get:", agentCurrent.keys)
            checkpointQueue.append(current)
        else:
            for hori, verti in directions:
                agentNext = copy.deepcopy(agentCurrent)
                # Check if the move is valid using the move function
                if world.move(hori, verti, agentNext):
                    if tuple(agentNext.pos) in visited:
                        continue
                    queue.append(Node(parent = current, agents = agentNext, g = current.g + 1, h = agentNext.MED()))
                    visited.add(tuple(agentNext.pos))

    return checkpointQueue

def decisionSearch(world):
    agent = world.agents["A1"]
    queue = PriorityQueue()
    queue.put(Node(agents = agent))
    while queue.empty() != True:
        current = queue.get()
        # agentCurrent = current.agents
        # current.printState()
        if current.isGoal() == True:
            return current

        checkpointQueue = searchKey(current, world)

        while checkpointQueue:
            nodeNext = checkpointQueue.pop(0)
            queue.put(nodeNext)

    return None