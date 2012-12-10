from AbstractGrid import AbstractGrid

class Crossword(AbstractGrid):
    """ Class extends empty abstract grid with ability to work with input dictionary words"""

    def fill_with_words(self, word_list):
        return self.__dfs(self.horizontal_words[0], word_list)

    def __validate_grid(self):
        for word in self.horizontal_words:
            for cross in self.vertical_words:
                if word.check_cross(cross):
                    if cross.value is not None and word.value is not None and not word.check_cross_value(cross):
                        return False
        return True

    def __dfs(self, root, available_dict):
        copied_dict = available_dict[0:]
        is_right = False

        for word in root.get_right_words(available_dict):
            root.value = word
            if self.__validate_grid():
                is_right = True
                copied_dict.remove(word)
                for child in root.children:
                    is_right &= self.__dfs(child, copied_dict)
                    filled_words = self.__get_filled_words(child)
                    copied_dict = [item for item in copied_dict if item not in filled_words]
                if is_right:
                    return True
                else:
                    copied_dict.extend(self.__get_filled_words(root))
                    self.__clean_up(root)
        return is_right

    def __clean_up(self, root):
        root.value = None
        for child in root.children:
            self.__clean_up(child)

    def __get_filled_words(self, root):
        values = [root.value] if root.value is not None else []
        for child in root.children:
            values.extend(self.__get_filled_words(child))
        return values