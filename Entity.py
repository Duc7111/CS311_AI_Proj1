
class Entity():
    pos = [0, 0, 0]

    def __init__(self, f: int, n: int, m: int) -> None:
        self.pos[0] = f
        self.pos[1] = n
        self.pos[2] = m


class Agent(Entity):
    def __init__(self, f: int, n: int, m: int) -> None:
        super().__init__(f, n, m)
        self.task = None
        self.keys = {}

    def _move(self, hori: int, verti: int) -> None:
        self.pos[1] += hori
        self.pos[0] += verti
    
    def addTask(self, task: Entity) -> bool:
        if self.task is None:
            self.task = task
            return True
        return False

    # Mahadtan distance, overestimate the true cost since diagnal move count 1
    def MD(self) -> int: 
        return abs(self.pos[0] - self.goal[0]) + abs(abs(self.pos[1] - self.goal[1]))
    
    # Euclidean distance, still overestimate the true cost
    def ED(self) -> int:
        return int((abs(self.pos[0] - self.goal[0])**2 + abs(abs(self.pos[1] - self.goal[1]))**2)**0.5)

    # Combine two types, admissible
    def MED(self) -> int:
        return max(abs(self.pos[0] - self.goal[0]), abs(abs(self.pos[1] - self.goal[1])))

class Key(Entity):
    def __init__(self, f: int, n: int, m: int, door: Entity) -> None:
        super().__init__(f, n, m)
        self.door = door

