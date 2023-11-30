from World import World
from Algo import bfs
world = World("input1-level1.txt")
print(world.agents["A1"].pos)
print(world.agents["A1"].task.pos)
final = bfs(world)
print(final.agents.pos)
final = bfs(world)
if final is None:
    print("Cannot find a path to Mr.T!")
else:
    print("Path travelled:")
    while final is not None:
        print(final.agents.pos)
        final = final.parent