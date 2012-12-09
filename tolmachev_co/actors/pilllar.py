from actors.actor import Actor

class Pillar (Actor):
    NAME = "Pillar"

    def accept_visitor(self, visitor):
        visitor.visit_pillar(self)

    def get_name(self):
        return NAME