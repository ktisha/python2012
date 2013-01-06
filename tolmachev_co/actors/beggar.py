from actors.actor import Actor

class BeggarState:
    SEARCHING_A_BOTTLE = 1
    WALKING_WITH_A_BOTTLE = 2
    AT_THE_TAVERN = 3

class Beggar (Actor):
    TAVERN_TIMEOUT = 40

    def __init__(self, tavern_coordinate):
        self.__current_state = BeggarState.SEARCHING_A_BOTTLE
        self.__tavern_coordinate = tavern_coordinate
        self.__counter = 0

    def accept_visitor(self, visitor):
        visitor.visit_beggar(self)

    def is_searching_a_bottle(self):
        return self.__current_state == BeggarState.SEARCHING_A_BOTTLE

    def is_walking_with_a_bottle(self):
        return self.__current_state == BeggarState.WALKING_WITH_A_BOTTLE

    def is_in_tavern(self):
        return self.__current_state == BeggarState.AT_THE_TAVERN

    def spend_time_in_tavern(self):
        self.__counter += 1

    def is_ready_to_search_a_bottle(self):
       return self.__counter == Beggar.TAVERN_TIMEOUT

    def start_searching_a_bottle(self):
        self.__counter = 0
        self.__current_state = BeggarState.SEARCHING_A_BOTTLE

    def start_walking_with_bottle(self):
        self.__current_state = BeggarState.WALKING_WITH_A_BOTTLE

    def start_to_be_in_tavern(self):
        self.__current_state = BeggarState.AT_THE_TAVERN

    def get_tavern_coordinate(self):
        return self.__tavern_coordinate