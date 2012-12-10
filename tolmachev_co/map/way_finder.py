from coordinate import Coordinate

class WayFinder:
    def __init__(self, map, start, end):
        self.__map = map
        self.__start = start
        self.__end = end

    def get_path(self, end_vertex):
        path = []
        vertex = end_vertex
        while vertex.get_prev_vertex().get_coordinate() != vertex.get_coordinate():
            path.append(vertex.get_coordinate())
            vertex = vertex.get_prev_vertex()
        path.reverse()
        return path

    def find_path(self):
        v = Vertex(self.__start, None, 0)
        v.set_prev_vertex(v)
        front = [self.__start]
        visited = [self.__start]

        map = {}
        map[self.__start] = v

        next_front = []

        while True:

            for front_coord in front:
                if front_coord in self.__end:
                    end_vertex = map[front_coord]
                    return self.get_path(end_vertex)

                neighbours = self.__get_neighbours(front_coord)
                for neighbour in neighbours:
                    if not neighbour in visited:
                        next_front.append(neighbour)
                        visited.append(neighbour)

                        front_vertex = map[front_coord]
                        neighbour_vertex = Vertex(neighbour, front_vertex, front_vertex.get_layer() + 1)
                        map[neighbour] = neighbour_vertex

            front = next_front
            next_front = []
            if not front :
                return []
        return []

    def __get_neighbours(self, coord):
        left = Coordinate(coord.get_x() - 1, coord.get_y())
        right = Coordinate(coord.get_x() + 1, coord.get_y())
        up = Coordinate(coord.get_x(), coord.get_y() + 1)
        down = Coordinate(coord.get_x(), coord.get_y() - 1)
        candidates = [left, right, up, down]

        neighbours = []
        for coord in candidates:
            if self.__map.is_in_bounds(coord) and self.__map.is_empty_field_except_sleeping_alcoholic(coord):
                neighbours.append(coord)
        return neighbours


class Vertex:
    def __init__(self, coordinate, prev_vertex, layer):
        self.__coordinate = coordinate
        self.__prev_vertex = prev_vertex
        self.__layer = layer

    def get_layer(self):
        return self.__layer

    def get_prev_vertex(self):
        return self.__prev_vertex

    def get_coordinate(self):
        return self.__coordinate

    def set_prev_vertex(self, prev_vertex):
        self.__prev_vertex = prev_vertex


