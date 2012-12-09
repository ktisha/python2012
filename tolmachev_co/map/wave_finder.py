
class WaveFinder :

    def __init__(self, map, start, end):
        self.__map = map
        self.__start = start
        self.__end = end

    def find_path(self) :
        __end
        front = [policeman_coord]
        visited = [policeman_coord]
        next_front = []

        for front_coord in front :
            neighbours = self.__get_neighbours(front_coord)
            if


    def __get_neighbours(self, coord):
        left = Coordinate(coord.get_x() - 1, coord.get_y())
        right = Coordinate(coord.get_x() + 1, coord.get_y())
        up = Coordinate(coord.get_x(), coord.get_y() + 1)
        down = Coordinate(coord.get_x(), coord.get_y() - 1)
        candidates = [left, right, up, down]

        neighbour = []
        for coord in candidates :
            if self.is_in_bounds(coord) :
                neighbour += coord