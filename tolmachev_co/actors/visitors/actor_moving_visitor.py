from actors.alcoholic import Alcoholic
from actors.bottle import Bottle
from actors.pilllar import Pillar
from actors.visitors.actor_visitor import ActorVisitor
import random
from map.coordinate import Coordinate


class ActorMovingVisitor(ActorVisitor):
    class MovingDirection:
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    def __init__(self, map):
        self.__map = map

    def visit_alcoholic(self, alcoholic, coordinate):
        def try_make_step(coordinate):
            direction = random.randint(0, 3)
            if direction == ActorMovingVisitor.MovingDirection.LEFT:
                return Coordinate(coordinate.get_x() - 1, coordinate.get_y())
            elif direction == ActorMovingVisitor.MovingDirection.RIGHT:
                return Coordinate(coordinate.get_x() + 1, coordinate.get_y())
            elif direction == ActorMovingVisitor.MovingDirection.DOWN:
                return Coordinate(coordinate.get_x(), coordinate.get_y() - 1)
            else:
                return Coordinate(coordinate.get_x(), coordinate.get_y() + 1)

        if alcoholic.is_awake():
            new_coord = try_make_step(coordinate)
            if self.__map.is_in_bounds(new_coord):
                actor = self.__map[new_coord]
                if not actor:
                    del self.__map[coordinate]
                    self.__map[new_coord] = alcoholic
                elif isinstance(actor, Bottle) or isinstance(actor, Pillar) or\
                     (isinstance(actor, Alcoholic) and actor.is_sleeping()):
                    alcoholic.make_asleep()
                else:
                    pass

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

