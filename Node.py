from Entity import Agent

class Node:
    def __init__(self, parent=None, agents = [], g=0, h=0):
        self.parent = parent
        self.agents = agents
        self.g = g
        self.h = h

    def printState(self):
        print(self.agents.pos, " ", self.g)

    def isGoal(self) -> bool:
        if self.agents.pos != self.agents.task.pos:
            return False
        return True

    def __eq__(self, other):
        return self.agents.pos == other.agents.pos

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)