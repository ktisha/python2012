from Crossword import Crossword

file = open("grid.txt")
input_grid = []
for line in file.readlines():
    input_grid.append(line.split())
file.close()

file = open("dict.txt")
input_dict = []
for line in file.readlines():
    input_dict.extend(line.split())
file.close()

# TODO: add exception handling for: working with files, validate input - grid's format

crossword = Crossword()
crossword.parse_matrix(input_grid)
is_right = crossword.fill_with_words(input_dict)

if is_right:
    for word in crossword.horizontal_words:
        if word.value is not None:
            input_grid[word.item][word.start : word.end + 1] = word.value
    for word in crossword.vertical_words:
        if word.value is not None:
            for line in input_grid:
                if word.start <= input_grid.index(line) <= word.end:
                    line[word.item] = word.value[input_grid.index(line) - word.start]
    for line in input_grid:
        print line
else:
    print "Error! Can not fill crossword with that dictionary!"








