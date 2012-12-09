from actors.actor import Actor

class AlcoholicState:
    IS_AWAKE = 1
    IS_SLEEPING = 2
    IS_CAUGHT_BY_POLICEMAN = 3

class Alcoholic (Actor):
    def __init__(self):
        self.__current_state = AlcoholicState.IS_AWAKE
        self.__has_bottle = True

    def accept_visitor(self, visitor):
        visitor.visit_alcoholic(self)

    def get_current_state(self):
        return self.__current_state

    def has_bottle(self):
        return self.__has_bottle