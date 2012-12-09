from actors.bottle import Bottle
from actors.visitors.actor_visitor import ActorVisitor
import random
from map.coordinate import Coordinate


class ActorMovingVisitor (ActorVisitor):
    class MovingDirection:
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    def __init__(self, map):
        self.__map = map

    def visit_alcoholic(self, alcoholic, coordinate):
        def try_make_step(self, coordinate) :
            direction = random.randint(0, 3)
            if direction == ActorMovingVisitor.MovingDirection.UP :
                return Coordinate(coordinate.get_x() - 1, coordinate.get_y())
            elif direction == 2 :
                return Coordinate(coordinate.get_x() + 1, coordinate.get_y())
            elif direction == 3 :
                return Coordinate(coordinate.get_x(), coordinate.get_y() - 1)
            else :
                return Coordinate(coordinate.get_x(), coordinate.get_y() + 1)

        if alcoholic.is_awake() :
            new_coord = try_make_step(coordinate)
            if self.__map.is_in_bounds(new_coord) :
                actor = self.__map[new_coord]
                if actor == None :
                    self.__map[coordinate] = None
                    self.__map[new_coord] = alcoholic
                elif actor.get_name() == Bottle.NAME :




    def visit_beggar(self, beggar, coordinate):
        pass

    def visit_pillar(self, pillar, coordinate):
        pass

    def visit_lamp(self, lamp, coordinate):
        pass

    def visit_bottle(self, bottle, coordinate):
        pass

    def visit_policeman(self, policeman, coordinate):
        pass

