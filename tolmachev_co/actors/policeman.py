from actors.actor import Actor

class PolicemanState:
    IS_AT_THE_STATION = 1
    IS_WALKING_TO_ALCOHOLIC = 2
    IS_WALKING_WITH_ALCOHOLIC = 3

class Policeman (Actor):
    def __init__(self):
        self.__current_state = PolicemanState.IS_AT_THE_STATION

    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)

    def is_at_the_station(self):
        return self.__current_state == PolicemanState.IS_AT_THE_STATION

    def is_walking_to_alcoholic(self):
        return self.__current_state == PolicemanState.IS_WALKING_TO_ALCOHOLIC

    def is_walking_with_alcoholic(self):
        return self.__current_state == PolicemanState.IS_WALKING_WITH_ALCOHOLIC
