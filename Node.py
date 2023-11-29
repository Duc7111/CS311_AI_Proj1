class Node:
    def __init__(self, parent=None, pos=[], g=0, h=0):
        self.parent = parent
        self.pos = pos
        self.g = g
        self.h = h

    def printState(self):
        print(self.pos, " ", self.g + self.h)

    def isGoal(self, goalPos) -> bool:
        if self.pos == goalPos:
            return True
        return False

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)