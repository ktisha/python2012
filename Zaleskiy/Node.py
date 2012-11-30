__author__ = 'glandike'
import Coordinates

class Node:

    map

    def __init__(self, coordinates, bombs, distance_from_start, parent, action):
        self.coordinates = coordinates
        self.bombs = bombs
        self.distance_from_start = distance_from_start
        self.distance_to_goal = self.coordinates.distance_between(Node.map.goal_coordinates)
        self.parent = parent
        self.action = action

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.score() < other.score()
        return 0

    def score(self):
        return self.distance_from_start+self.distance_to_goal

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coordinates == other.coordinates and self.bombs == other.bombs
    def __hash__(self):
        return self.bombs*1000000 + self.coordinates.x*1000 + self.coordinates.y

    def get_neighbours(self):
        move_right = Node(self.coordinates.right_coordinates(), self.bombs, self.distance_from_start+1, self, 'right')
        move_left = Node(self.coordinates.left_coordinates(), self.bombs, self.distance_from_start+1, self, 'left')
        move_up = Node(self.coordinates.up_coordinates(), self.bombs, self.distance_from_start+1, self, 'up')
        move_down = Node(self.coordinates.down_coordinates(), self.bombs, self.distance_from_start+1, self, 'down')

        boom_right = Node(self.coordinates.right_coordinates(), self.bombs-1, self.distance_from_start+1, self, 'crash right')
        boom_left = Node(self.coordinates.left_coordinates(), self.bombs-1, self.distance_from_start+1, self, 'crash left' )
        boom_up = Node(self.coordinates.up_coordinates(), self.bombs-1, self.distance_from_start+1, self, 'crash up')
        boom_down = Node(self.coordinates.down_coordinates(), self.bombs-1, self.distance_from_start+1, self, 'crash down')
        neighbour_list = []
        if Node.map.get_up_cell(self.coordinates) in (' ', 'E'):
            neighbour_list.append(move_up)
        elif Node.map.get_up_cell(self.coordinates) == '#' and self.bombs > 0:
            neighbour_list.append(boom_up)
        if Node.map.get_right_cell(self.coordinates) in (' ', 'E'):
            neighbour_list.append(move_right)
        elif Node.map.get_right_cell(self.coordinates) == '#' and self.bombs > 0:
            neighbour_list.append(boom_right)
        if Node.map.get_down_cell(self.coordinates) in (' ', 'E'):
            neighbour_list.append(move_down)
        elif Node.map.get_down_cell(self.coordinates) == '#' and self.bombs > 0:
            neighbour_list.append(boom_down)
        if Node.map.get_left_cell(self.coordinates) in (' ', 'E'):
            neighbour_list.append(move_left)
        elif Node.map.get_left_cell(self.coordinates) == '#' and self.bombs > 0:
            neighbour_list.append(boom_left)
        return neighbour_list


            