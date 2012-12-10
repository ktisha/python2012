from Crossword import Crossword
import sys

input_grid = []
input_dict = []

try:
    if len(sys.argv) != 3:
        print "Error: Wrong count of parameters!"
        exit(1)

    file = open(sys.argv[1])
    for line in file.readlines():
        input_grid.append(line.split())
    file.close()

    file = open(sys.argv[2])
    for line in file.readlines():
        input_dict.extend(line.split())
    file.close()

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
        print "Can not fill crossword with that dictionary!"

except IOError as e:
    print "Error: ", e.strerror, e.filename
except TypeError:
    print "Error: wrong format of the input crossword grid - empty or contains wrong chars!"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise








