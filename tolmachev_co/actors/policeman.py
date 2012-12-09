from actors.actor import Actor

class PolicemanState:
    IS_IN_STATION = 1
    IS_WALKING_TO_ALCOHOLIC = 2
    IS_WALKING_WITH_ALCOHOLIC = 3

class Policeman (Actor):
    def __init__(self):
        self.__current_state = PolicemanState.IS_IN_STATION

    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)
