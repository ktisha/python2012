class Coordinate:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def __hash__(self):
        return (self.__x, self.__y).__hash__()

    def __eq__(self, other):
        if not other:
            return False
        elif not isinstance(other, Coordinate):
            return False
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __cmp__(self, other):
        if self.get_x() < other.get_x():
            return -1
        elif self.get_x() == other.get_x():
            if self.get_y() < other.get_y():
                return -1
            elif self.get_y() == other.get_y():
                return 0
            else:
                return 1
        else:
            return 1
