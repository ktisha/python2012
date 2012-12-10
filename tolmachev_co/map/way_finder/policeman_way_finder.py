from actors.alcoholic import Alcoholic
from way_finder import WayFinder

class PolicemanWayFinder(WayFinder):
    def __init__(self, map, start, end):
        WayFinder.__init__(self, map, start, end)


    def valid_field_to_step(self, coordinate) :
        if self._map.has_actor_at(coordinate):
            actor = self._map.get(coordinate)
            if isinstance(actor, Alcoholic) :
                if actor.is_sleeping() :
                    return True
            return False
        else :
            return True

