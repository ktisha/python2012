from actors.actor import Actor

class Pillar (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_pillar(self)
