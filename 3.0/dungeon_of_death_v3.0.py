import json
import os
from player_state import player
from room_encounters import fight_monster, compelling_choices, ominous_encounter, trap_encounter, healing_fountain, exit_encounter
from shop_encounters import mythical_shop, tanky_shop
from dungeon_generation import generate_dungeon, find_entrance, SHOP_ROOMS, HEALING_ROOMS, FILLER_ROOMS, ENCOUNTER_ROOMS_NON_CB, COMBAT_ROOMS



script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")
rooms_file_path = os.path.join(script_dir, "rooms.json")

with open(monster_db_file_path, 'r') as file:
    monster_db = json.load(file)

with open(rooms_file_path, 'r') as file:
    room_data = json.load(file)


ENCOUNTER_HANDLERS = {
    "compelling_choices": compelling_choices,
    "ominous_encounter": ominous_encounter,
    "trap_encounter": trap_encounter,
    "mythical_shop": mythical_shop,
    "tanky_shop": tanky_shop,
    "healing_fountain": healing_fountain,
    "exit_encounter": exit_encounter
}


dungeon = generate_dungeon(20, 5)
entrance_y, entrance_x = find_entrance(dungeon)

visited = [[False for _ in row] for row in dungeon]
visited[entrance_y][entrance_x] = True

cleared = [[False for _ in row] for row in dungeon]
cleared[entrance_y][entrance_x] = True

player['position'] = (entrance_y, entrance_x)


def move_player(direction):
    y, x = player['position']
    no_room_msg = "No room in that direction, you run into a wall."

    if direction == "w":
        if y > 0:
            player['position'] = (y - 1, x)
            return True
        else:
            print(no_room_msg)
            return False
    elif direction == "s":
        if y < len(dungeon) - 1:
            player['position'] = (y + 1, x)
            return True
        else:
            print(no_room_msg)
            return False
    elif direction == "a":
        if x > 0:
            player['position'] = (y, x - 1)
            return True
        else:
            print(no_room_msg)
            return False
    elif direction == "d":
        if x < len(dungeon[0]) - 1:
            player['position'] = (y, x + 1)
            return True
        else:
            print(no_room_msg)
            return False


def enter_room():
    y, x = player['position']
    room = dungeon[y][x]
    visited[y][x] = True

    room_info = room_data.get(room)
    encounter = room_info.get("encounter")
    description = room_info.get("description")
    item = room_info.get("item")

    if not room_info:
        print("You step into an uncharted room. It's eerily empty.")
        return
    
    # Voi käyttää kauppoja vaikka olis cleared
    if cleared[y][x] and room not in SHOP_ROOMS:
        print("\033[1;32mRoom cleared.\033[0m")
        return

    if room != "Dungeon Exit":
        print(f"\033[1;35mYou move into the {room}.\033[0m\n")

    # Ei ylimäärästä linebreakkia filler huoneille
    if room not in FILLER_ROOMS:
        if description:
            print(description + "\n")
    else:
        if description:
            print(description)
    
    # Laukasee huoneen encounterin
    if encounter:
        handler = ENCOUNTER_HANDLERS.get(encounter)
        if handler:
            handler()
        else:
            fight_monster(monster_db[encounter])

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
    print(f"Equipped armor: \033[1;36m{player['armor']}\033[0m (remaining protection: \033[1;31m{player['armor_hp']}\033[0m)")
    

def check_inventory():
    print(f"Equipped weapon: \033[1;36m{player['weapon']}\033[0m (Max Hit: \033[1;31m{player['max_hit']}\033[0m)")
    print(f"Gold coins: \033[1;33m{player['gold']}\033[0m")
    print("Your bag:")
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;92m{item}\033[0m x{count}")
        else:
            print(f"\033[1;92m{item}\033[0m")
    print(f"\nTotal monster parts: \033[1;32m{sum(player['inventory'].values())}\033[0m")


def show_map():
    for y, row in enumerate(dungeon):
        row_display = []
        for x, room in enumerate(row):
            if (y, x) == player['position']:
                base_cell = f"▶ {dungeon[y][x]}"
                formatted_cell = f"{base_cell:<18}"
                cell = f"\033[94m{formatted_cell}\033[0m"
            elif visited[y][x]:
                cell = room
            else:
                cell = "???"
            row_display.append(f"{cell:<18}")
        print(" | " + " | ".join(row_display) + " | ")



def game_loop():
    print("\033[1;35mWelcome to the Dungeon of Death, adventurer!\033[0m")
    print("You are at the dungeon entrance and have to delve into the dungeon.\n")
    show_map()
    while True:
        command = input("\nEnter command | up(w) / down(s) / right(d) / left(a), health(h) / inventory(i) / map(m), quit |: ").lower()

        if command in ["w", "s", "a", "d"]:
            moved = move_player(command)
            if moved:
                enter_room()
            print()
            show_map()
        elif command == "m":
            print()
            show_map()
        elif command == "h":
            check_health()
        elif command == "i":
            check_inventory()
        elif command == "quit":
            print("Goodbye, adventurer.")
            break
        else:
            print("Invalid command")




if __name__ == "__main__":
    game_loop()