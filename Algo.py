from World import World
from queue import PriorityQueue
from Node import Node
from Entity import Agent
import copy

# direction to move
directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]


# Level 1 algorithms
def bfs(world):
    agent = world.agents["A1"]

    queue = [Node(agents=agent)]
    visited = set()
    visited.add(tuple(agent.pos))
    steps = []  # Store the visited positions

    while queue:
        current = queue.pop(0)
        agentCurrent = current.agents
        steps.append(agentCurrent.pos)

        if current.isGoal() == True:
            return current, steps

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.append(Node(parent=current, agents=agentNext))
                visited.add(tuple(agentNext.pos))

    return None, steps


def UCS(world):
    agent = world.agents["A1"]

    queue = PriorityQueue()
    queue.put(Node(agents=agent))
    visited = set()
    steps = []  # Store the visited positions

    while not queue.empty():
        current = queue.get()
        agentCurrent = current.agents
        steps.append(agentCurrent.pos)

        if tuple(agentCurrent.pos) in visited:
            continue

        visited.add(tuple(agentCurrent.pos))

        if current.isGoal():
            return current, steps

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.put(Node(parent=current, agents=agentNext, g=current.g + 1))

    return None, steps


def Astar(world):
    agent = world.agents["A1"]

    queue = PriorityQueue()
    queue.put(Node(agents=agent))
    visited = set()
    steps = []  # Store the visited positions

    while not queue.empty():
        current = queue.get()
        agentCurrent = current.agents
        steps.append(agentCurrent.pos)

        if tuple(agentCurrent.pos) in visited:
            continue

        visited.add(tuple(agentCurrent.pos))

        if current.isGoal():
            return current, steps

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[0], agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.deepcopy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.put(Node(parent=current, agents=agentNext, g=current.g + 1, h=agentNext.MED()))

    return None, steps

# Level 2 + 3:
def searchKey(currentState: Node, world: World):
    queue = [currentState]
    visited = set()
    visited.add(tuple(currentState.agents.pos))
    checkpointQueue = []

    while queue:
        current = queue.pop(0)
        agentCurrent = current.agents

        # Find a key or goal
        if current.isGoal() == True:
            checkpointQueue.append(current)
            return checkpointQueue
        if agentCurrent.keys != currentState.agents.keys:
            checkpointQueue.append(current)
        # If not, continue moving
        else:
            for hori, verti in directions:
                agentNext = copy.deepcopy(agentCurrent)
                # Check if the move is valid using the move function
                if world.move(hori, verti, agentNext):
                    if tuple(agentNext.pos) in visited:
                        continue
                    queue.append(Node(parent=current, agents=agentNext, g=current.g + 1, h=agentNext.MED()))
                    visited.add(tuple(agentNext.pos))

    return checkpointQueue


def decisionSearch(world, agent="A1"):
    agent = world.agents[agent]
    queue = PriorityQueue()
    queue.put(Node(agents=agent))

    while queue.empty() != True:
        current = queue.get()

        # Reach goal -> stop
        if current.isGoal() == True:
            return current

        # Generate successors
        checkpointQueue = searchKey(current, world)

        while checkpointQueue:
            nodeNext = checkpointQueue.pop(0)
            queue.put(nodeNext)
    return None


# Path reader
def pathReader(final) -> list:
    path = []
    while final is not None:
        path.insert(0, final.agents.pos)
        final = final.parent
    return path if len(path) > 0 else None
