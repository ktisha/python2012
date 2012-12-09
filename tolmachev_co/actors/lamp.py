from actors.actor import Actor

class Lamp (Actor):
    def __init__(self, lighting_radius = 3):
        self.__lighting_radius = lighting_radius

    def accept_visitor(self, visitor):
        visitor.visit_lamp(self)

    def get_lighting_radius(self):
        return self.__lighting_radius