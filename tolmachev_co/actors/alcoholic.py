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

    def is_awake(self):
        return self.__current_state == AlcoholicState.IS_AWAKE

    def is_sleeping(self):
        return self.__current_state == AlcoholicState.IS_SLEEPING

    def is_caught_by_policeman(self):
        return self.__current_state == AlcoholicState.IS_CAUGHT_BY_POLICEMAN

    def has_bottle(self):
        return self.__has_bottle