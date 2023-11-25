from World import World

def bfs(world):
    agent = world.agents[0]
    task = agent.task

    queue = [(agent.pos, [])]
    visited = set()

    while queue:
        pos, path = queue.pop(0)

        if pos == task.pos:
            return path

        if pos in visited:
            continue

        visited.add(pos)

        for hori, verti in [(0, 1), (0, -1), (1, 0), (-1, 0)]:#Not checking the diagonal movement
            new_pos = [pos[0] + verti, pos[1] + hori]

            if world.move(verti, hori):
                new_path = path + [(new_pos, world._check(verti, hori))]
                queue.append((new_pos, new_path))

    return None