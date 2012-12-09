from actors.actor import Actor
from actors.bottle import Bottle

class AlcoholicState:
    AWAKE = 1
    SLEEPING = 2
    CAUGHT_BY_POLICEMAN = 3

class Alcoholic (Actor):
    def __init__(self):
        self.__current_state = AlcoholicState.AWAKE
        self.__has_bottle = True

    def accept_visitor(self, visitor):
        visitor.visit_alcoholic(self)

    def is_awake(self):
        return self.__current_state == AlcoholicState.AWAKE

    def is_sleeping(self):
        return self.__current_state == AlcoholicState.SLEEPING

    def is_caught_by_policeman(self):
        return self.__current_state == AlcoholicState.CAUGHT_BY_POLICEMAN

    def has_bottle(self):
        return self.__has_bottle

    def make_asleep(self):
        self.__current_state = AlcoholicState.SLEEPING

    def drop_a_bottle(self):
        self.__has_bottle = False
        return Bottle()

    def draw(self):
        print 'A',