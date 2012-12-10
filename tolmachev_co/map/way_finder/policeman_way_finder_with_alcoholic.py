from way_finder import WayFinder

class PolicemanWayFinderWithAlcoholic(WayFinder):
    def __init__(self, map, start, end):
        WayFinder.__init__(self, map, start, end)


    def valid_field_to_step(self, coordinate) :
        if self._map.has_actor_at(coordinate):
            return False
        else :
            return True