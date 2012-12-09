from actors.actor import Actor

class BeggarState:
    SEARCHING_A_BOTTLE = 1
    WALKING_WITH_A_BOTTLE = 2
    AT_THE_TAVERN = 3

class Beggar (Actor):
    NAME = "Beggar"

    def __init__(self):
        self.__current_state = BeggarState.SEARCHING_A_BOTTLE

    def accept_visitor(self, visitor):
        visitor.visit_beggar(self)

    def get_name(self):
        return NAME

    def is_searching_a_bottle(self):
        return self.__current_state == BeggarState.SEARCHING_A_BOTTLE

    def is_walking_with_a_bottle(self):
        return self.__current_state == BeggarState.WALKING_WITH_A_BOTTLE

    def is_in_tavern(self):
        return self.__current_state == BeggarState.AT_THE_TAVERN