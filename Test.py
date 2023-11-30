from World import World
from Algo import bfs, UCS, Astar
world = World("input1_level1.txt")
print(world.agents["A1"].pos)
print(world.agents["A1"].task.pos)
final = bfs(world)
print(final.agents.pos)
final1 = bfs(world)
final2 = UCS(world)
final3 = Astar(world)
if final1 is None:
    print("Cannot find a path to Mr.T!")
else:
    print("Path travelled:")
    while final1 is not None:
        print(final1.agents.pos, " ", final2.agents.pos, " ", final3.agents.pos)
        final1 = final1.parent
        final2 = final2.parent
        final3 = final3.parent