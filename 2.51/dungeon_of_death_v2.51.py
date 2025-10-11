import random
import json
import os
from dungeon_layouts import dungeons
from player_state import player
from room_encounters import fight_monster, mythical_shop, compelling_choices, ominous_encounter, trap_encounter, exit_encounter



script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")
rooms_file_path = os.path.join(script_dir, "rooms.json")

with open(monster_db_file_path, 'r') as file:
    monster_db = json.load(file)

with open(rooms_file_path, 'r') as file:
    room_data = json.load(file)

dungeon = random.choice(dungeons)


visited = [[False for _ in row] for row in dungeon]
visited[0][0] = True

cleared = [[False for _ in row] for row in dungeon]
cleared[0][0] = True


def move_player(direction):
    y, x = player['position']

    if direction == 'w':
        if y > 0:
            player['position'] = (y-1, x)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 's':
        if y < len(dungeon) - 1:
            player['position'] = (y+1, x)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 'a':
        if x > 0:
            player['position'] = (y, x-1)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 'd':
        if x < len(dungeon[0]) - 1:
            player['position'] = (y, x+1)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False




def enter_room():
    y, x = player['position']
    room = dungeon[y][x]
    visited[y][x] = True

    room_info = room_data.get(room)
    encounter = room_info.get("encounter")
    description = room_info.get("description")

    if not room_info:
        print("You step into an uncharted room. It's eerily empty.")
        return
    
    # Voi käyttää kauppaa vaikka olis cleared
    if cleared[y][x] and room != "Mythical Shop":
        print("\033[1;32mRoom cleared.\033[0m")
        return

    if room != 'Dungeon Exit':
        print(f"\033[1;35mYou move into the {room}.\033[0m\n")

    # Ei ylimäärästä linebreakkia strange roomille
    if room != 'Strange Room':
        if description:
            print(description + '\n')
    else:
        if description:
            print(description)

    if encounter:
        if encounter == "compelling_choices":
            compelling_choices()
        elif encounter == "ominous_encounter":
            ominous_encounter()
        elif encounter == "trap_encounter":
            trap_encounter()
        elif encounter == "mythical_shop":
            mythical_shop()
        elif encounter == "exit_encounter":
            print('\033[1;35mYou have reached the Dungeon exit.\033[0m\n')
            exit_encounter()
        else:
            fight_monster(monster_db[encounter])

    item = room_info.get("item")
    if item:
        add_to_inventory(item)

    cleared[y][x] = True


def add_to_inventory(item):
    if item in player['inventory']:
        player['inventory'][item] += 1
    else:
        player['inventory'][item] = 1


def check_health():
    print(f"Your current health: \033[1;94m{player['health']}\033[0m")
    

def check_inventory():
    print(f"Equipped weapon: \033[1;36m{player['weapon']}\033[0m (Max Hit: \033[1;31m{player['max_hit']}\033[0m)")
    print(f"Gold coins: \033[1;33m{player['gold']}\033[0m")
    print('Your bag:\n')
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;92m{item}\033[0m x{count}")
        else:
            print(f"\033[1;92m{item}\033[0m")


def show_map():
    for y, row in enumerate(dungeon):
        row_display = []
        for x, room in enumerate(row):
            if (y, x) == tuple(player['position']):
                cell = f"▶ {dungeon[y][x]}"
            elif visited[y][x]:
                cell = room
            else:
                cell = '???'
            row_display.append(f"{cell:<18}")
        print(' | ' + ' | '.join(row_display))
    
    y, x = player['position']



def game_loop():
    print('\033[1;35mWelcome to the Dungeon of Death, adventurer!\033[0m')
    print('You are at the dungeon entrance and have to delve into the dungeon.\n')
    show_map()
    while True:
        command = input('\nEnter command | up(w) / down(s) / right(d) / left(a), health(h) / inventory(i) / map(m), quit |: ').lower()

        if command in ['w', 's', 'a', 'd']:
            moved = move_player(command)
            if moved:
                enter_room()
            print()
            show_map()
        elif command == 'm':
            print()
            show_map()
        elif command == 'h':
            check_health()
        elif command == 'i':
            check_inventory()
        elif command == 'quit':
            print('Goodbye, adventurer.')
            break
        else:
            print('Invalid command')



if __name__ == "__main__":
    game_loop()
