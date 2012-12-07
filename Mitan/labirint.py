import sys

import pygame
import string

pygame.init()

def BFS(G, start, end):
    #G is graph in format [N, E]. N is number of vertices, E - list of edges
    #in format [[a, b], ...]
    # start end - vertices that we are looking for way between
    is_visited, dist, prev = {}, {}, {}
    #standard BFS
    for current in [x for x in range(G[0]) if x != start]:
        is_visited[current], dist[current], prev[current] = False, "inf", None
    is_visited[start], dist[start], prev[start] = True, 0, None
    Q = [] # queue
    Q.append(start)
    while Q != []:
        current = Q.pop(0)
        for neighbour in [x[1] for x in G[1] if x[0] == current]:
            if is_visited[neighbour] == False:
                is_visited[neighbour], dist[neighbour], prev[neighbour] = True, dist[current] + 1, current
                Q.append(neighbour)
        is_visited[current] = True
    path = [] # path from start to end
    current = prev[end]
    while current is not None:
        path.insert(0, current)
        current = prev[current]
    return (is_visited[end], dist[end], path)

def draw_a_line(window, color, startx, starty, orientation):
    """Draws a line of length 1 cell in window starting in startx starty"""
    #start_x start_y end_x end_y coordinats of start and end of line
    start_x = ed_pix * (1 + startx)
    start_y = ed_pix * (1 + starty)
    if orientation == 0:
        end_x = ed_pix * (2 + startx)
        end_y = ed_pix * (1 + starty)
    else:
        end_x = ed_pix * (1 + startx)
        end_y = ed_pix * (2 + starty)
    if color == "black":
        pygame.draw.line(window, (0, 0, 0), (start_x, start_y), (end_x, end_y), 6)
        #dafuq with width = 3 doesn't work for black
    elif color == "white":
        pygame.draw.line(window, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)
    elif color == "green":
        pygame.draw.line(window, (0, 255, 0), (start_x, start_y), (end_x, end_y), 3)

def draw_entrance_and_exit(window, st_end, rows):
    """Draws entrance and exit of labirint in window"""
    answer = []
    for line in st_end:
        split_line = map(int, string.split(line))
        if split_line[0] == 0:
            draw_a_line(window, "black", split_line[0], split_line[1], 1)
        elif split_line[0] == cols - 1:
            draw_a_line(window, "black", split_line[0] + 1, split_line[1], 1)
        elif split_line[1] == 0:
            draw_a_line(window, "black", split_line[0], split_line[1], 0)
        elif split_line[1] == rows - 1:
            draw_a_line(window, "black", split_line[0], split_line[1] + 1, 0)
        cell = rows * split_line[0] + split_line[1]
        answer.append(cell)
    #in answer we get two ints - ord numbers of entrance and exit cells
    return answer

def draw_an_arrow(window, x, y, orientation):
    """Draws a small arrow in the center of cell with coordinates x and y"""
    # x and y a coordinates of cell where to draw an arrow
    #orientation is angle to rotate  arrow
    size = int(round(0.5 * ed_pix))
    #arrow_surface - small surface to draw arrow
    arrow_surface = pygame.Surface((size, size))
    #lots of coordinates
    startx = int(round(size * 0.2))
    endx = int(round(size * 0.8))
    starty = int(round(size * 0.5))
    endy = int(round(size * 0.5))
    starty2 = int(round(size * 0.4))
    starty3 = int(round(size * 0.6))
    startx2 = int(round(size * 0.7))
    pygame.draw.line(arrow_surface, (255, 0, 0), (startx, starty), (endx, endy), 1)
    pygame.draw.line(arrow_surface, (255, 0, 0), (startx2, starty2), (endx, endy), 1)
    pygame.draw.line(arrow_surface, (255, 0, 0), (startx2, starty3), (endx, endy), 1)
    arrow_surface = pygame.transform.rotate(arrow_surface, orientation)
    screenx = int(round((x + 1.25) * ed_pix))
    screeny = int(round((y + 1.25) * ed_pix))
    window.blit(arrow_surface, (screenx, screeny))
def is_in_field(i, j):
    """Check if the cell with cordinates i j is in labirint"""
    answer  = False
    if i in range(cols) and j in range(rows):
        answer = True
    return answer

def create_empty_labirint_graph(cols, rows):
    """Creates graph of a labirint with no walls inside"""
    edges = []
    # number of vertices in graph
    vertices = cols * rows
    for n in range(vertices):
        #coordinates of cell
        i = n // rows
        j = n % rows
        if is_in_field(i - 1, j):
            edges[0:0] = [[n, n - rows]]
        if is_in_field(i + 1, j):
            edges[0:0] = [[n, n + rows]]
        if is_in_field(i, j + 1):
            edges[0:0] = [[n, n + 1]]
        if is_in_field(i, j - 1):
            edges[0:0] = [[n, n - 1]]
    return edges

def check_wall(window, first, next):
    """Check if there is a wall between cells first and next"""
    # first and next are ord numbers of cells
    is_wall = False
    orientation = 0
    diff = next - first
    if [first, next] in walls:
        startx = next // rows
        starty = next % rows
        is_wall = True
        if diff == 1:
            draw_a_line(window, "green", startx, starty, 0)
        elif diff == -1:
            draw_a_line(window, "green", startx, starty  + 1, 0)
        elif diff == rows:
            draw_a_line(window, "green", startx, starty, 1)
        elif diff == - rows:
            draw_a_line(window, "green", startx + 1, starty, 1)
    if diff == 1:
        orientation = 270
    elif diff == -1:
        orientation = 90
    elif diff == rows:
        pass
    elif diff == - rows:
        orientation = 180
    return is_wall, orientation

input_strings = open(sys.argv[1], 'r').readlines()
cr_string = map(int, string.split(input_strings[0]))
#in first string cols  rows bombs of labirint
cols, rows, bombs = cr_string
#length of single cell
ed_pix = 80
#rows and cols of window
w_cols, w_rows = ed_pix * (cols + 2), ed_pix * (rows + 2)
#window to display
window = pygame.display.set_mode((w_cols, w_rows))
#draw borders of labirint
labirint_edges = pygame.Rect(ed_pix, ed_pix, cols * ed_pix, rows * ed_pix)
pygame.draw.rect(window, (255, 255, 255), labirint_edges, 3)
#in 2 and 3 strings position of start and end
#cells take numbers from zero to col-1
#start and finish a numbers of cells near entrance and exit
start = draw_entrance_and_exit(window, input_strings[1:3], rows)[0]
finish = draw_entrance_and_exit(window, input_strings[1:3], rows)[1]
# edges is a graph of labirint wwith no walls
edges = create_empty_labirint_graph(cols, rows)
# walls - list of forbidden edges - between these pairs of cells there are walls
walls = []
#in next strings 1-cell walls in format x y orientation
#x and y are coordinates of cell which is lower or righter from the edge
#orientation is zero if it's horizontal and 1 if vertical
for str in input_strings[3:]:
    line = map(int, string.split(str))
    draw_a_line(window, "white", line[0], line[1], line[2])
    current_cell = rows * line[0] + line[1]
    if line[2] == 0:       
        edges.remove([current_cell, current_cell - 1])
        edges.remove([current_cell - 1, current_cell])
        walls[0:0] = [[current_cell, current_cell - 1], [current_cell - 1, current_cell]]
    else:
        edges.remove([current_cell, current_cell  - rows])
        edges.remove([current_cell - rows, current_cell])
        walls[0:0] = [[current_cell, current_cell  - rows], [current_cell - rows, current_cell]]
#construct a 3d graph with k levels
edges_3d_graph  = []
vertices_3d_graph = (bombs + 1) * cols * rows
# constructing edges of 3d graph
for edge in edges:
    for i in range(bombs + 1):
        edges_3d_graph.append([i * cols * rows + edge[0], i * cols * rows + edge[1]])
for edge in walls:
    for i in range(bombs):
        edges_3d_graph.append([i * cols * rows + edge[0], (i + 1) * cols * rows + edge[1]])
# make a new virtual vertice connected with finish cells of all levels
for i in range(bombs + 1):
    edges_3d_graph.append([i * cols * rows + finish, vertices_3d_graph])
    edges_3d_graph.append([vertices_3d_graph, i * cols * rows + finish])
#3d graph of labirint
Ghraph_3d = [vertices_3d_graph + 1, edges_3d_graph]
#BFS gives as output[2] path from start to finish

if BFS(Ghraph_3d, start, vertices_3d_graph)[0]:
    #path to exit
    path = map (lambda x: x % (cols * rows), BFS(Ghraph_3d, start, vertices_3d_graph)[2])
    for k in path:
        if path.index(k) != len(path) - 1:
            next = path[path.index(k) + 1]
            #check if there is a wall and color it with green
            check_wall(window, k, next)
            #orientation of way to next cell
            next_orientation = check_wall(window, k, next)[1]
            x_cord = k // rows
            y_cord = k % rows
            draw_an_arrow(window, x_cord, y_cord, next_orientation)
    #for finish we need special arrow-orientation
    finishx  = finish // rows
    finishy = finish % rows
    finish_orientation = 0
    if finishx == 0:
        finish_orientation = 180
    elif  finishx == cols - 1:
        pass
    elif  finishy == rows - 1:
        finish_orientation = 270
    elif  finishy == 0:
        finish_orientation = 90
    draw_an_arrow(window, finishx, finishy, finish_orientation)
else:
    myfont = pygame.font.SysFont(None, ed_pix)
    label = myfont.render("NO WAY, DUDE!", 1, (255, 0, 0))
    window.blit(label, (ed_pix, 0))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
