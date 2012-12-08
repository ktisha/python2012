class Map:
    DEFAULT_WIDTH = 15
    DEFAULT_HEIGHT = 15

    def __init__(self):
        self.__init__(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__actors_dict = {}

    def draw(self):
        pass

    def next_move(self):
        pass


