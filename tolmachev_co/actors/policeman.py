from actors.actor import Actor

class PolicemanState:
    AT_THE_STATION = 1
    WALKING_TO_ALCOHOLIC = 2
    WALKING_WITH_ALCOHOLIC = 3

class Policeman (Actor):
    NAME = "Policeman"

    def __init__(self):
        self.__current_state = PolicemanState.AT_THE_STATION

    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)

    def get_name(self):
        return NAME

    def is_at_the_station(self):
        return self.__current_state == PolicemanState.AT_THE_STATION

    def is_walking_to_alcoholic(self):
        return self.__current_state == PolicemanState.WALKING_TO_ALCOHOLIC

    def is_walking_with_alcoholic(self):
        return self.__current_state == PolicemanState.WALKING_WITH_ALCOHOLIC
