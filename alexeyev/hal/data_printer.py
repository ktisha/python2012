__author__ = 'Anton M Alexeyev'

import converter

def graph_to_file(matrix, list, file_path):
    """
        To be removed. Proved unsuccessful :(
    """
    file = open(file_path, "w")
    file.write("nodedef>")
    file.write("name INT, label VARCHAR\n")

    dict = {}

    i = 1
    for key in list:
        file.write(str(i) + ", \"" + key + "\"\n")
        dict[key] = i
        i += 1

    file.write("edgedef>")
    file.write("source INT, target INT, weight DOUBLE\n")
    for key0 in list:
        for key1 in list:
            if key0 <> key1:
                file.write(
                    str(dict[key0])
                    + ", "
                    + str(dict[key1])
                    + ", "
                    # exponential hardcode
                    + str(100 ** matrix.dist_cols_inverted_cosine(
                        converter.get_token_by_word(key0), converter.get_token_by_word(key1))) + "\n")
    file.close()

#todo: vector representation, dimension reduction
"""
def vectors_to_file(matrix, list, file_path):

    file = open(file_path, "w")
    for key in list:
        pass

    file.close()
"""