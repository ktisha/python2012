from actors.alcoholic import Alcoholic
from actors.bottle import Bottle
from actors.pilllar import Pillar
from actors.visitors.actor_visitor import ActorVisitor
import random
from map.coordinate import Coordinate
from map.way_finder.policeman_way_finder import PolicemanWayFinder
from map.way_finder.policeman_way_finder_with_alcoholic import PolicemanWayFinderWithAlcoholic

class ActorMovingVisitor(ActorVisitor):
    class MovingDirection:
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    def __init__(self, map, actor_coordinate):
        self.__map = map
        self.__actor_coordinate = actor_coordinate

    def visit_alcoholic(self, alcoholic):
        def try_make_step(coordinate):
            direction = random.randint(0, 3)
            if direction == ActorMovingVisitor.MovingDirection.LEFT:
                return Coordinate(coordinate.get_x() - 1, coordinate.get_y())
            elif direction == ActorMovingVisitor.MovingDirection.RIGHT:
                return Coordinate(coordinate.get_x() + 1, coordinate.get_y())
            elif direction == ActorMovingVisitor.MovingDirection.DOWN:
                return Coordinate(coordinate.get_x(), coordinate.get_y() - 1)
            else:
                return Coordinate(coordinate.get_x(), coordinate.get_y() + 1)

        def should_drop_a_bottle():
            random_number = direction = random.randint(1, 30)
            return random_number == 30

        coordinate = self.__actor_coordinate
        if alcoholic.is_awake():
            new_coord = try_make_step(coordinate)
            if self.__map.is_in_bounds(new_coord):
                if not self.__map.has_actor_at(new_coord):
                    self.__map.remove(coordinate)
                    self.__map.put(new_coord, alcoholic)
                    if should_drop_a_bottle() and alcoholic.has_bottle():
                        bottle = alcoholic.drop_a_bottle()
                        self.__map.put(coordinate, bottle)
                else:
                    actor = self.__map.get(new_coord)
                    if isinstance(actor, Bottle) or isinstance(actor, Pillar) or\
                       (isinstance(actor, Alcoholic) and actor.is_sleeping()):
                        alcoholic.make_asleep()
                    else:
                        pass


    def visit_beggar(self, beggar):
        pass


    def visit_pillar(self, pillar):
        pass


    def visit_lamp(self, lamp):
        pass


    def visit_bottle(self, bottle):
        pass


    def visit_policeman(self, policeman):
        if policeman.is_at_the_station():
            dict = self.__map.get_lightened_sleeping_alcos()
            if dict:
                policeman.start_walking_to_alcoholic()

        if policeman.is_walking_to_alcoholic():
            coordinate = self.__map.get_policeman_coord()
            dict = self.__map.get_lightened_sleeping_alcos()
            wayFinder = PolicemanWayFinder(self.__map, coordinate, dict.keys())
            new_coord = wayFinder.get_next_coordinate_to_go()
            if new_coord:
                if  self.__map.has_actor_at(new_coord):
                    policeman.start_walking_with_alcoholic()
                self.__map.remove(coordinate)
                self.__map.put(new_coord, policeman)

        if policeman.is_walking_with_alcoholic():
            coordinate = self.__map.get_policeman_coord()
            end_coords = [policeman.get_station_coordinate()]
            wayFinder = PolicemanWayFinderWithAlcoholic(self.__map, coordinate, end_coords)
            new_coord = wayFinder.get_next_coordinate_to_go()
            if new_coord:
                if  new_coord in end_coords:
                    policeman.start_to_be_at_station()
                self.__map.remove(coordinate)
                self.__map.put(new_coord, policeman)


    def visit_tavern(self, tavern):
        if tavern.is_time_to_generate_alcoholic():
            coordinate = Coordinate(0, 9)
            if not self.__map.has_actor_at(coordinate):
                alcoholic = tavern.generate_alcoholic()
                self.__map.put(coordinate, alcoholic)
        tavern.increase_steps_number_after_alcoholic_generation()



