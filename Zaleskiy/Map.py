__author__ = 'glandike'
import Coordinates

class Map:



    def __init__(self, path):
        try:
            self.path_to_map = path
            self.map = [[line.strip('\n\t')] for line in open(path)]
        except IOError:
            print "You have printed wrong path to file or file name. Be more attentive."
            exit()
        self.find_goal_and_start_coordinates()

    def __str__(self):
        for line in open(self.path_to_map):
            print line.strip('\n\t')
        return ''
    def find_goal_and_start_coordinates(self):
        find_goal = False
        find_start = False
        for i in xrange(len(self.map)):
            for j in xrange(len(self.map[i][0])):
                if self.map[i][0][j] == 'E':
                    self.goal_coordinates = Coordinates.Coordinates(j,i)
                    find_goal = True
                if self.map[i][0][j] == 'T':
                    self.start_coordinates = Coordinates.Coordinates(j,i)
                    find_start = True
                if find_goal and find_start:
                    return

    def get_right_cell(self,coordinates): # 1 - empty 2 - wall 3 - exit 0 -error
        return self.get_cell_at(coordinates.right_coordinates())

    def get_left_cell(self,coordinates): # 1 - empty 2 - wall 3 - exit 0 -error
        return self.get_cell_at(coordinates.left_coordinates())

    def get_up_cell(self,coordinates): # 1 - empty 2 - wall 3 - exit 0 -error
        return self.get_cell_at(coordinates.up_coordinates())

    def get_down_cell(self,coordinates): # 1 - empty 2 - wall 3 - exit 0 -error
        return self.get_cell_at(coordinates.down_coordinates())

    def get_cell_at(self, coordinates):
        if coordinates.getX() > 0 and coordinates.getX() < len(self.map[coordinates.getY()][0])-1 and coordinates.getY() > 0 and coordinates.getY() < len(self.map)-1:
            if self.map[coordinates.getY()][0][coordinates.getX()] in (' ', '#', 'E', 'T'):
                return self.map[coordinates.getY()][0][coordinates.getX()]
            else:
                raise TypeError('Map contains wrong character! Please check the map.')
        else:
            return None
