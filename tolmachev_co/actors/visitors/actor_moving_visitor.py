from actors.visitors.actor_visitor import ActorVisitor
import random
from map.coordinate import Coordinate


class ActorMovingVisitor (ActorVisitor):
    def __init__(self, map):
        self.__map = map

    def visit_alcoholic(self, alcoholic, coordinate):
        if alcoholic.is_awake() :
            x_step = random.randrange(-1, 1, 1)
            y_step = random.randrange(-1, 1, 1)
            step = Coordinate(x_step, y_step)


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
