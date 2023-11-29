from World import World
from queue import PriorityQueue

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
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for hori, verti in directions:
            new_pos = [pos[0] + verti, pos[1] + hori]

            # Check if the move is valid using the move function
            if world.move(verti, hori):
                new_path = path + [(new_pos, world._check(verti, hori))]
                if pos in visited:
                    continue
                queue.append((new_pos, new_path))

    return None
