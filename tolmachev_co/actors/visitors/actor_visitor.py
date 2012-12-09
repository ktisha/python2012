class ActorVisitor:
    def visit_alcoholic(self, alcoholic, coordinate):
        raise NotImplementedError("Abstract method is called")

    def visit_beggar(self, beggar, coordinate):
        raise NotImplementedError("Abstract method is called")

    def visit_bottle(self, bottle, coordinate):
        raise NotImplementedError("Abstract method is called")

    def visit_lamp(self, lamp, coordinate):
        raise NotImplementedError("Abstract method is called")

    def visit_pillar(self, pillar, coordinate):
        raise NotImplementedError("Abstract method is called")

    def visit_policeman(self, policeman, coordinate):
        raise NotImplementedError("Abstract method is called")
