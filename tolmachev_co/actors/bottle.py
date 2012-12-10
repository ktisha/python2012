from actors.actor import Actor

class Bottle (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_bottle(self)
