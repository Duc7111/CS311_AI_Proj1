from World import World
from Algo import bfs
world = World("input1-level1.txt")
print(world.agents["A1"].pos)
print(world.agents["A1"].task.pos)
# bfs(world)