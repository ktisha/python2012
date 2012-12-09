from actors.actor import Actor

class Bottle (Actor):
    NAME = "Bottle"

    def accept_visitor(self, visitor):
        visitor.visit_bottle(self)

    def get_name(self):
        return NAME