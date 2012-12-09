from actors.beggar import Beggar
from actors.lamp import Lamp
from actors.pilllar import Pillar
from actors.policeman import Policeman
from actors.visitors.actor_moving_visitor import ActorMovingVisitor
from map.coordinate import Coordinate

class Map:
    DEFAULT_WIDTH = 15
    DEFAULT_HEIGHT = 15

    __actors_dictionary = {}
    __width = 0
    __height = 0

    def __init__(self):
        self.__init__(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__actors_dictionary[Coordinate(7, 7)] = Pillar()
        self.__actors_dictionary[Coordinate(3, 10)] = Lamp()
        self.__actors_dictionary[Coordinate(3, 15)] = Policeman()
        self.__actors_dictionary[Coordinate(15, 4)] = Beggar()

    def get(self, coordinate):
        return self.__actors_dictionary[coordinate]

    def put(self, coordinate, actor):
        self.__actors_dictionary[coordinate] = actor

    def remove(self, coordinate):
        del self.__actors_dictionary[coordinate]

    def draw(self):
        for x in xrange(0, self.__width):
            for y in xrange(0, self.__height):
                coordinate = Coordinate(x, y)
                if coordinate in self.__actors_dictionary:
                    actor = self.__actors_dictionary[coordinate]
                    actor.draw()
                else:
                    print ' ',
            print

    def next_move(self):
        for coordinate, actor in self.__actors_dictionary.keys(), self.__actors_dictionary.values():
            moving_visitor = ActorMovingVisitor(self, coordinate)
            actor.accept_visitor(moving_visitor)

    def is_in_bounds(self, coordinate):
        return 0 <= coordinate.get_x() < self.__width and 0 <= coordinate.get_y() < self.__height
