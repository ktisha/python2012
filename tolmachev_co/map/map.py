from actors.beggar import Beggar
from actors.lamp import Lamp
from actors.pilllar import Pillar
from actors.policeman import Policeman
from map.coordinate import Coordinate

class Map:
    DEFAULT_WIDTH = 15
    DEFAULT_HEIGHT = 15

    def __init__(self):
        self.__init__(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__actors_dictionary = {}
        self.__actors_dictionary[Coordinate(7, 7)] = Pillar()
        self.__actors_dictionary[Coordinate(3, 10)] = Lamp()
        self.__actors_dictionary[Coordinate(3, 15)] = Policeman()
        self.__actors_dictionary[Coordinate(15, 4)] = Beggar()

    def draw(self):
        pass

    def next_move(self):
        pass

    def is_in_bounds(self, coordinate):
        if coordinate.get_x() >= 0 and coordinate.get_x() < self.__width and\
           coordinate.get_y() >= 0 and coordinate.get_y() < self.__height:
            return True
        else:
            return False


