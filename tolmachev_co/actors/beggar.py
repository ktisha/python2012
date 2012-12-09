from actors.actor import Actor

class BeggarState:
    IS_SEARCHING_A_BOTTLE = 1
    IS_WALKING_WITH_A_BOTTLE = 2
    IS_IN_TAVERN = 3

class Beggar (Actor):
    def __init__(self):
        self.__current_state = BeggarState.IS_SEARCHING_A_BOTTLE

    def accept_visitor(self, visitor):
        visitor.visit_beggar(self)

    def is_searching_a_bottle(self):
        return self.__current_state == BeggarState.IS_SEARCHING_A_BOTTLE

    def is_walking_with_a_bottle(self):
        return self.__current_state == BeggarState.IS_WALKING_WITH_A_BOTTLE

    def is_in_tavern(self):
        return self.__current_state == BeggarState.IS_IN_TAVERN