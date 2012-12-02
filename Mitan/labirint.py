import sys
import pygame
import string

pygame.init()

def BFS(G, start, end):
    is_visited, dist, prev = {}, {}, {}
    for u in [x for x in range(G[0]) if x != start]:
        is_visited[u], dist[u], prev[u] = False, "inf", None
    is_visited[start], dist[start], prev[start] = True, 0, None
    Q = [] # queue
    Q.append(start)
    while Q != []:
        u = Q.pop(0)
        for v in [x[1] for x in G[1] if x[0] == u]:
            if is_visited[v] == False:
                is_visited[v], dist[v], prev[v] = True, dist[u] + 1, u
                Q.append(v)
        is_visited[u] = True
    path = []
    current = prev[end]
    while current != None:
        path.insert(0, current)
        current = prev[current]
    return (is_visited[end], dist[end], path)

def draw_a_line(window, color, startx, starty, orientation):
    """Draws a line of length 1 cell in window starting in startx starty"""
    global ed_pix
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
    """Draws entrance and exit in window"""
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
    #in answer we get to ints - ord numbers of entrance and exit cells
    return answer
def draw_a_circle(window, x, y):
    """Draws a small circle in the center of cell with coordinates x and y"""
    global ed_pix
    center_x = int (round ((x + 1.5) * ed_pix))
    center_y = int(round ((y + 1.5) * ed_pix))
    radius = int (round(ed_pix * 0.1))
    pygame.draw.circle(window, (255, 0, 0), (center_x, center_y), radius)
def create_empty_labirint_graph(cols, rows):
    """Creates graph of a labirints with no walls inside"""
    edges = []
    #cells connected with corner cells
    edges[0:0]  = [[0, 1], [0, rows]]
    edges[0:0]  = [[rows - 1, 2 * rows - 1], [rows - 1, rows - 2]]
    edges[0:0]  = [[rows * (cols - 1), rows * (cols - 2)], [rows * (cols - 1), rows * (cols - 1) + 1]]
    edges[0:0]  = [[rows * cols - 1, rows * cols - 2], [rows * cols - 1, rows * (cols - 1) - 1]]
    #cells near the border
    for i in range(1, cols - 1):
        edges[0:0]  = [[rows * i, rows * (i - 1)], [rows * i, rows * (i + 1)], [rows * i, rows * i + 1]]
        edges[0:0]  = [[rows * (i + 1) - 1, rows * i - 1], [rows * (i + 1) - 1, rows * (i + 2) - 1], [rows * (i + 1) - 1, rows * (i + 1) - 2]]
    for i in range(1, rows - 1):
        edges[0:0]  = [[i, i - 1], [i, i + 1], [i, rows + i]]
        edges[0:0]  = [[rows * (cols - 1) + i, rows * (cols - 1) + i - 1], [rows * (cols - 1) + i, rows * (cols - 1) + i + 1], [rows * (cols - 1) + i, rows * (cols - 2) + i]]
    # Not border cells
    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            edges[0:0]  = [[rows * i + j, rows * i + j - 1], [rows * i + j, rows * i + j + 1]]
            edges[0:0]  = [[rows * i + j, rows * (i - 1) + j], [rows * i + j, rows * (i + 1) + j]]
    return edges

input_strings = open('input.txt', 'r').readlines()
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
#in next strings 1-cell edges in format x y orientation
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
for edge in edges:
    for i in range(bombs + 1):
        edges_3d_graph.append([i * cols * rows + edge[0], i * cols * rows + edge[1]])
for edge in walls:
    for i in range(bombs):
        edges_3d_graph.append([i * cols * rows + edge[0], (i + 1 ) * cols * rows + edge[1]])
# make a new virtual vertice connected with finish cells of all levels
for i in range(bombs + 1):
    edges_3d_graph.append([i * cols * rows + finish, vertices_3d_graph])
    edges_3d_graph.append([vertices_3d_graph,i * cols * rows + finish ])
#3d graph of labirint
Ghraph_3d = [vertices_3d_graph + 1 , edges_3d_graph]
#BFS gives as output[2] path from start to finish
for k in BFS(Ghraph_3d, start, vertices_3d_graph)[2]:
    k = k % (cols * rows)
    i = k // rows
    j = k % rows
    draw_a_circle(window, i, j)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
