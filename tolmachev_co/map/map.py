from actors.alcoholic import Alcoholic
from actors.beggar import Beggar
from actors.bottle import Bottle
from actors.lamp import Lamp
from actors.pilllar import Pillar
from actors.policeman import Policeman
from actors.tavern import Tavern
from actors.visitors.actor_drawing_visitor import ActorDrawingVisitor
from actors.visitors.actor_moving_visitor import ActorMovingVisitor
from coordinate import Coordinate

class Map:
    __actors_dictionary = {}

    def __init__(self, width=15, height=15):
        self.__width = width
        self.__height = height
        self.__actors_dictionary[Coordinate(7, 7)] = Pillar()
        self.__actors_dictionary[Coordinate(3, 10)] = Lamp()
        self.__actors_dictionary[Coordinate(3, 15)] = Policeman(Coordinate(3, 15))
        self.__actors_dictionary[Coordinate(15, 4)] = Beggar(Coordinate(15, 4))
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

    def get_lamps(self):
        lamps = {}
        for y in xrange(0, self.__height):
            for x in xrange(0, self.__width):
                coordinate = Coordinate(x, y)
                if coordinate in self.__actors_dictionary:
                    actor = self.__actors_dictionary[coordinate]
                    if isinstance(actor, Lamp):
                        lamps[coordinate] = actor
        return lamps

    def get_lightened_sleeping_alcos(self):
        lamps = self.get_lamps()
        lamps_coord = lamps.keys()

        sleeping_alcoholics = {}
        for lamp_coord in lamps_coord :
            lamp = lamps[lamp_coord]
            for lightened_y in xrange(lamp_coord.get_y() - lamp.get_lighting_radius(), lamp_coord.get_y() + lamp.get_lighting_radius() + 1):
                for lightened_x in xrange(lamp_coord.get_x() - lamp.get_lighting_radius(), lamp_coord.get_x() + lamp.get_lighting_radius() + 1):
                    lightened_coordinate = Coordinate(lightened_x, lightened_y)
                    if lightened_coordinate in self.__actors_dictionary:
                        lightened_actor = self.__actors_dictionary[lightened_coordinate]
                        if isinstance(lightened_actor, Alcoholic):
                            if lightened_actor.is_sleeping() :
                                sleeping_alcoholics[lightened_coordinate] = lightened_actor
        return sleeping_alcoholics

    def get_bottles(self):
        bottles = {}
        for y in xrange(0, self.__height):
            for x in xrange(0, self.__width):
                coordinate = Coordinate(x, y)
                if coordinate in self.__actors_dictionary:
                    actor = self.__actors_dictionary[coordinate]
                    if isinstance(actor, Bottle):
                        bottles[coordinate] = actor
        return bottles

    def get_policeman_coord(self):
        coordinates = self.__actors_dictionary.keys()
        actors = self.__actors_dictionary.values()
        for coordinate, actor in zip(coordinates, actors):
            if isinstance(actor, Policeman) :
               return coordinate

    def get_beggar_coord(self):
        coordinates = self.__actors_dictionary.keys()
        actors = self.__actors_dictionary.values()
        for coordinate, actor in zip(coordinates, actors):
            if isinstance(actor, Beggar) :
                return coordinate




