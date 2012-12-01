__author__ = 'glandike'

class Coordinates:

    def __init__(self,*args):
        if len(args) == 1:
            if isinstance(args[0], Coordinates):
                self.x = args[0].getX()
                self.y = args[0].getY()
        else:
            self.x = args[0]
            self.y = args[1]

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + '\n'
    def distance_between(self, node):
        return  abs(node.x - self.x) + abs(node.y - self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def right_coordinates(self):
        return Coordinates(self.getX() + 1, self.getY())

    def left_coordinates(self):
        return Coordinates(self.getX() - 1, self.getY())

    def up_coordinates(self):
        return Coordinates(self.getX(), self.getY() - 1)

    def down_coordinates(self):
        return Coordinates(self.getX(), self.getY() + 1)