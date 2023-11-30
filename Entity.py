
class Entity():
    pos = [0, 0, 0]

    def __init__(self, f: int, n: int, m: int) -> None:
        self.pos = [f, n, m]


class Agent(Entity):
    def __init__(self, f: int, n: int, m: int) -> None:
        super().__init__(f, n, m)
        self.task = None
        self.keys = {}

    def _move(self, verti: int, hori: int) -> None:
        self.pos[1] += verti
        self.pos[2] += hori

    # Mahadtan distance, overestimate the true cost since diagnal move count 1
    def MD(self) -> int: 
        return abs(self.pos[1] - self.task[1]) + abs(abs(self.pos[2] - self.task[2]))
    
    # Euclidean distance, still overestimate the true cost
    def ED(self) -> int:
        return int((abs(self.pos[1] - self.task[1])**2 + abs(abs(self.pos[2] - self.task[2]))**2)**0.5)

    # Combine two types, admissible
    def MED(self) -> int:
        return abs(self.pos[0] - self.task.pos[0]) + max(abs(self.pos[1] - self.task.pos[1]), abs(abs(self.pos[2] - self.task.pos[2])))

class Key(Entity):
    def __init__(self, f: int, n: int, m: int) -> None:
        super().__init__(f, n, m)
        self.doors = []

