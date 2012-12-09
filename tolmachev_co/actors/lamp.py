from actors.actor import Actor

class Lamp (Actor):
    NAME = "Lamp"

    def accept_visitor(self, visitor):
        visitor.visit_lamp(self)

    def get_name(self):
        return NAME