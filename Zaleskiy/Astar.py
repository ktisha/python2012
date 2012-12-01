__author__ = 'glandike'
import Map, Node
from heapq import heappop, heappush

def search_path_by_a_star():
    closed_nodes = {}
    open_nodes = {}
    queue_of_nodes = []
    path = raw_input("Enter path to the map :\n(For example 'map1.map')\n")
    map = Map.Map(path)
    print map
    bombs = int(raw_input("Enter amount of bombs\n"))
    map.find_goal_and_start_coordinates()
    Node.Node.map = map
    start = Node.Node(map.start_coordinates, bombs, 0, None, None)
    heappush(queue_of_nodes, start)
    while len(queue_of_nodes) > 0:
        next_node = heappop(queue_of_nodes)
        open_nodes[next_node] = next_node.score()
        closed_nodes[next_node] = next_node.score()
        if next_node.coordinates == map.goal_coordinates:
            iter = next_node
            path = []
            while iter.coordinates != map.start_coordinates:
                path.append(iter.action)
                iter = iter.parent
            path.reverse()
            return path
        for neighbour in next_node.get_neighbours():
            if closed_nodes.has_key(neighbour):
                continue
            if open_nodes.has_key(neighbour):
                if open_nodes.get(neighbour)< neighbour.score():
                    open_nodes.pop(neighbour)
                    open_nodes[neighbour] = neighbour.score()
                else:
                    continue
            open_nodes[neighbour] = neighbour.score()
            heappush(queue_of_nodes, neighbour)

    return 'No possible ways to exit from labyrinth'

print search_path_by_a_star()



