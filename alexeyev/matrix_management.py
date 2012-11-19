__author__ = 'Anton M Alexeyev'

class WordMatrix:
    """
    Sparse matrix presented as a dictionary "(token0, token1)->value".
    Implementation may change later.
    """
    def __init__(self):
        self.matrix = {("", ""):0}
        self.token_set = []

    def add(self, first_token, second_token, value):
        """Adds given value to the given cell"""
        if not self.matrix.has_key((first_token, second_token)):
            self.matrix[(first_token, second_token)] = 0
        self.matrix[(first_token, second_token)] += value
        if not first_token in self.token_set:
            self.token_set += [first_token]
        if not second_token in self.token_set:
            self.token_set += [second_token]

    def get(self, first_token, second_token):
        """Gets cell with given coords"""
        if not self.matrix.has_key((first_token, second_token)):
            return 0
        return self.matrix[(first_token, second_token)]

    def get_tokens(self):
        """Gets all the tokens in stock"""
        return self.token_set

    #todo: euclidean distance
    def dist_cols_euclidean(self, col0, col1):
        """Measures distance between 2 columns: Euclidean distance"""
        pass

    #todo: cosine similarity
    def dist_cols_cosine(self, col0, col1):
        """Measures distance between 2 columns: Cosine similarity"""
        pass

    #todo: knn for cols
    def knc(self, target_column, k, dist_func):
        """Gets k nearest columns to target_column by distance function provided by dist_func"""
        pass