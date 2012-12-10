from Word import Word

class AbstractGrid:
    """ Presents structure of a grid, contains lists of horizontal and vertical words without words"""
    def __init__(self):
        self.horizontal_words = []
        self.vertical_words = []

    def __extract_words_coordinates(self, list):
        words_coordinates = []
        j = 0 # index of current cell
        length = len(list)
        while j < length:
            while j < length and list[j] == '_':
                j += 1
            if j != length:
                x1 = j
                while j < length and list[j] == '*':
                    j += 1
                x2 = j - 1
                if x2 - x1 > 1:
                    words_coordinates.append((x1, x2))
        return words_coordinates

    def parse_matrix(self, matrix):
        self.__check_format(matrix)
        for i in xrange(len(matrix)):
            words_coordinates = self.__extract_words_coordinates(matrix[i])
            for (x1, x2) in words_coordinates:
                self.horizontal_words.append(Word(i, x1, x2))
        for j in xrange(len(matrix[0])):
            vertical_list = [list[j] for list in matrix]
            words_coordinates = self.__extract_words_coordinates(vertical_list)
            for (y1, y2) in words_coordinates:
                self.vertical_words.append(Word(j, y1, y2))
        self.__build_tree(self.horizontal_words[0], False)

    def __build_tree(self, parent, is_vertical):
        parent.flag = 1
        cross_list = self.horizontal_words if is_vertical else self.vertical_words
        for cross in cross_list:
            if cross.flag != 1 and parent.check_cross(cross):
                parent.children.append(self.__build_tree(cross, not is_vertical))
        return parent

    def __check_format(self, list):
        if len(list) == 0:
            raise TypeError
        for line in list:
            isRight = True
            for i in line:
                isRight &= i == '*' or i == '_'
            if not isRight:
                raise TypeError