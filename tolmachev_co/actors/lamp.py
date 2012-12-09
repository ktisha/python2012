from actors.actor import Actor

class Lamp (Actor):
    def accept_visitor(self, visitor):
        visitor.visit_lamp(self)

    def draw(self):
        print 'o',