from actors.bottle import Bottle
from way_finder import WayFinder

class BeggarWayFinder(WayFinder):
    def __init__(self, map, start, end):
        WayFinder.__init__(self, map, start, end)


    def valid_field_to_step(self, coordinate) :
        if self._map.has_actor_at(coordinate):
            actor = self._map.get(coordinate)
            if isinstance(actor, Bottle) :
                return True
            return False
        else :
            return True