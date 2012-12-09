from actors.beggar import Beggar
from actors.lamp import Lamp
from actors.pilllar import Pillar
from actors.policeman import Policeman
from actors.tavern import Tavern
from actors.visitors.actor_drawing_visitor import ActorDrawingVisitor
from actors.visitors.actor_moving_visitor import ActorMovingVisitor
from coordinate import Coordinate

class Map:
    __actors_dictionary = {}

    def __init__(self, width = 15, height = 15):
        self.__width = width
        self.__height = height
        self.__actors_dictionary[Coordinate(7, 7)] = Pillar()
        self.__actors_dictionary[Coordinate(3, 10)] = Lamp()
        self.__actors_dictionary[Coordinate(3, 15)] = Policeman()
        self.__actors_dictionary[Coordinate(15, 4)] = Beggar()
        self.__actors_dictionary[Coordinate(-1, 9)] = Tavern()

    def has_actor_at(self, coordinate):
        return coordinate in self.__actors_dictionary

    def get(self, coordinate):
        return self.__actors_dictionary[coordinate]

    def put(self, coordinate, actor):
        self.__actors_dictionary[coordinate] = actor

    def remove(self, coordinate):
        del self.__actors_dictionary[coordinate]

    def draw(self):
        drawing_visitor = ActorDrawingVisitor()
        for y in xrange(0, self.__height):
            for x in xrange(0, self.__width):
                coordinate = Coordinate(x, y)
                if coordinate in self.__actors_dictionary:
                    actor = self.__actors_dictionary[coordinate]
                    actor.accept_visitor(drawing_visitor)
                else:
                    print '_',
            print

    def next_move(self):
        coordinates = self.__actors_dictionary.keys()
        actors = self.__actors_dictionary.values()
        for coordinate, actor in zip(coordinates, actors):
            moving_visitor = ActorMovingVisitor(self, coordinate)
            actor.accept_visitor(moving_visitor)

    def is_in_bounds(self, coordinate):
        return 0 <= coordinate.get_x() < self.__width and 0 <= coordinate.get_y() < self.__height
