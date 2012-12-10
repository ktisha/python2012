import os
from map.map import Map

def main():
    game_map = Map(15, 15)

    while True:
        game_map.draw()
        game_map.next_move()

        c = raw_input()
        if c == "x":
            break

if __name__ == "__main__":
    main()