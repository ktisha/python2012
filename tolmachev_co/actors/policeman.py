from actors.actor import Actor

class Policeman (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_policeman(self)
