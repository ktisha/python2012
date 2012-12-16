from actors.actor import Actor

class PolicemanState:
    AT_THE_STATION = 1
    WALKING_TO_ALCOHOLIC = 2
    WALKING_WITH_ALCOHOLIC = 3


class Policeman(Actor):
    def __init__(self, station_coordinate):
        self.__current_state = PolicemanState.AT_THE_STATION
        self.__station_coordinate = station_coordinate

    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)

    def get_station_coordinate(self):
        return self.__station_coordinate

    def is_at_the_station(self):
        return self.__current_state == PolicemanState.AT_THE_STATION

    def is_walking_to_alcoholic(self):
        return self.__current_state == PolicemanState.WALKING_TO_ALCOHOLIC

    def is_walking_with_alcoholic(self):
        return self.__current_state == PolicemanState.WALKING_WITH_ALCOHOLIC

    def start_walking_to_alcoholic(self):
        self.__current_state = PolicemanState.WALKING_TO_ALCOHOLIC

    def start_walking_with_alcoholic(self):
        self.__current_state = PolicemanState.WALKING_WITH_ALCOHOLIC

    def start_to_be_at_station(self):
        self.__current_state = PolicemanState.AT_THE_STATION