from actors.actor import Actor

class BeggarState:
    IS_SEARCHING_A_BOTTLE = 1
    IS_WALKING_WITH_BOTTLE = 2
    IS_IN_POINT_FOR_GLASS = 3

class Beggar (Actor):
    def __init__(self):
        self.__current_state = BeggarState.IS_SEARCHING_A_BOTTLE

    def accept_visitor(self, visitor):
        visitor.visit_beggar(self)