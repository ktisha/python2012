import os
from map.map import Map

def main():
    game_map = Map(15, 15)

    game_map.draw()
#    while True:
#        c = raw_input()
#        if c == "x":
#            break
#        else:
#            os.system('clear')
#            game_map.draw()
#            game_map.next_move()

if __name__ == "__main__":
    main()