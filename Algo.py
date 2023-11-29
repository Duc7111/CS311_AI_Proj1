from World import World
from queue import PriorityQueue
from Node import Node

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

def bfs(world):
    agent = world.agents[0]
    task = agent.task

    queue = [(agent.pos, [])]
    visited = set()

    while queue:
        pos, path = queue.pop(0)

        if pos == task.pos:
            return path

        visited.add(pos)

        for hori, verti in directions:
            new_pos = [pos[0] + verti, pos[1] + hori]
            if new_pos in visited:
                continue
            # Check if the move is valid using the move function
            if world.move(verti, hori):
                new_path = path + [(new_pos, world._check(verti, hori))]
                queue.append((new_pos, new_path))

    return None


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
