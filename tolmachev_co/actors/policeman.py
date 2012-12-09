from actors.actor import Actor

class PolicemanState:
    IS_OBSERVING = 1
    IS_WALKING_TO_ALCO = 2
    IS_WALKING_WITH_ALCO = 3

class Policeman (Actor):
    def __init__(self):
        self.__current_state = PolicemanState.IS_OBSERVING

    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)
