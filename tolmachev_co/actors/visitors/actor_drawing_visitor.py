from actors.visitors.actor_visitor import ActorVisitor

class ActorDrawingVisitor(ActorVisitor):
    def visit_alcoholic(self, alcoholic):
        print 'A',

    def visit_beggar(self, beggar):
        print 'B',

    def visit_pillar(self, pillar):
        print '|',

    def visit_lamp(self, lamp):
        print 'O',

    def visit_bottle(self, bottle):
        print '~',

    def visit_policeman(self, policeman):
        print 'P',

    def visit_tavern(self, tavern):
        pass
