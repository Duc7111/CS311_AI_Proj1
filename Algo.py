from World import World
from queue import PriorityQueue
from Node import Node
import copy

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

def bfs(world):
    agent = world.agents["A1"]

    queue = [Node(agents = agent)]
    visited = set()

    while queue:
        current = queue.pop()
        agentCurrent = current.agents
        print(agentCurrent.pos)
        print(agentCurrent.task.pos)
        if current.isGoal == True:
            return current
        
        visited.add(tuple(agentCurrent.pos))
        print(agentCurrent.pos)

        for hori, verti in directions:
            new_pos = [agentCurrent.pos[1] + hori, agentCurrent.pos[2] + verti]
            if tuple(new_pos) in visited:
                continue
            agentNext = copy.copy(agentCurrent)
            # Check if the move is valid using the move function
            if world.move(hori, verti, agentNext):
                queue.append(Node(parent = agentCurrent, agents = agentNext))

    return False


def UCS(world):
    agent = world.agents[0]
    task = agent.task
    # Prepare for UCS
    frontier = PriorityQueue()
    frontier.put(Node(pos = agent.pos))
    visited = set()

    while frontier.empty() != True:
        # Get smallest in frontier and put to expanded list
        current = frontier.get()
        visited.add(current.pos)
        # If goal -> stop
        if current.isGoal(task.pos) == True:
            return current
        # Generate next state
        for hori, verti in directions:
            new_pos = [current.pos[0] + verti, current.pos[1] + hori]
            if new_pos in visited:
                continue
            # Check if the move is valid using the move function
            if world.move(verti, hori):
                new_path = path + [(new_pos, world._check(verti, hori))]
                frontier.put(Node(parent = current, pos = new_pos, g = current.g + 1))
        
    return None
