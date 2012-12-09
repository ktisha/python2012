from actors.actor import Actor
from actors.alcoholic import Alcoholic

class Tavern(Actor):
    ALCOHOLIC_GENERATION_FREQUENCY = 20

    def __init__(self):
        self.__steps_number_after_alcoholic_generation = 0

    def accept_visitor(self, visitor):
        visitor.visit_tavern(self)

    def draw(self):
        pass

    def is_time_to_generate_alcoholic(self):
        return self.__steps_number_after_alcoholic_generation == Tavern.ALCOHOLIC_GENERATION_FREQUENCY

    def increase_steps_number_after_alcoholic_generation(self):
        self.__steps_number_after_alcoholic_generation += 1

    def generate_alcoholic(self):
        self.__steps_number_after_alcoholic_generation = 0
        return Alcoholic()