
import numpy as np
import math as m

class Entity:
    pos = [0,0]
    goal = [0,0]
    np.ndarray
    pass

class Agent(Entity):

    def _move(self, hori: int, verti: int) -> None:
        self.pos[1] += hori
        self.pos[0] += verti

    def atGoal(self) -> bool:
        return self.pos == self.goal
    
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
    pass
