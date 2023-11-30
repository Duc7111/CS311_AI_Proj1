from Entity import Agent

class Node:
    def __init__(self, parent=None, agents = [], g=0, h=0):
        self.parent = parent
        self.agents = agents
        self.g = g
        self.h = h

    def printState(self):
        print(self.pos, " ", self.g + self.h)

    def isGoal(self) -> bool:
        for a in agents:
            if a.pos != a.task.pos:
                return False
        return True

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)