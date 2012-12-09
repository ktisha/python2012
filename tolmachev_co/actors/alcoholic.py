from actors.actor import Actor

class Alcoholic (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_alcoholic(self)