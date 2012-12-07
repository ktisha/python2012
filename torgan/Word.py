class Word:
    """
    Presents structure of a grid's word
        item - row(or column) at the grid
        start, end - start and end coordinates at row(column)
    """
    def __init__(self, item, start, end):
        self.item = item
        self.start = start
        self.end = end
        self.value = None
        self.children = []
        self.flag = 0 # ony for building tree

    def check_cross_value(self, word):
        if self.check_cross(word) :
            return self.value[word.item - self.start] == word.value[self.item - word.start]
        return True

    def check_cross(self, word):
        return word.start <= self.item <= word.end and self.start <= word.item <= self.end

    def get_right_words(self, word_list):
        result = [word for word in word_list if len(word) == self.end - self.start + 1]
        return result