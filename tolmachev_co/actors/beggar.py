from actors.actor import Actor

class Beggar (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_beggar(self)