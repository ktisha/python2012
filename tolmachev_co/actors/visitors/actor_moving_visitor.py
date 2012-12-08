from actors.visitors.actor_visitor import ActorVisitor

class ActorMovingVisitor (ActorVisitor):
    def __init__(self, map):
        self.__map = map

    def visit_alcoholic(self, alcoholic):
        pass

    def visit_beggar(self, beggar):
        pass

    def visit_pillar(self, pillar):
        pass

    def visit_lamp(self, lamp):
        pass

    def visit_bottle(self, bottle):
        pass

    def visit_policeman(self, policeman):
        pass
