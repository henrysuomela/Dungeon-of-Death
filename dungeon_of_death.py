import json
import os
import player_state as ps
import room_encounters as re
import shop_encounters as se
import dungeon_generation as dg


script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")
rooms_file_path = os.path.join(script_dir, "rooms.json")

with open(monster_db_file_path, 'r') as file:
    monster_db = json.load(file)

with open(rooms_file_path, 'r') as file:
    room_data = json.load(file)


ENCOUNTER_HANDLERS = {
    "compelling_choices": re.compelling_choices,
    "ominous_encounter": re.ominous_encounter,
    "trap_encounter": re.trap_encounter,
    "mythical_shop": se.mythical_shop,
    "tanky_shop": se.tanky_shop,
    "healing_fountain": re.healing_fountain,
    "exit_encounter": re.exit_encounter
}

def create_dungeon():
    dungeon = dg.generate_dungeon()
    entrance_y, entrance_x = dg.find_entrance(dungeon)
    entrance_coords = (entrance_y, entrance_x)
    ps.player['position'] = entrance_coords

    visited, cleared, missing_a_door, which_doors_missing = dg.create_helper_grids(dungeon)

    return {
        "dungeon": dungeon,
        "entrance_coords": entrance_coords,
        "visited": visited,
        "cleared": cleared,
        "missing_a_door": missing_a_door,
        "which_doors_missing": which_doors_missing
    }


def start_game():
    if ps.player is not None:
        ps.player.clear()
        ps.player.update(ps.create_player())
    else:
        ps.player = ps.create_player()

    dungeon_state = create_dungeon()
    return dungeon_state




def move_player(direction, dungeon_state):
    y, x = ps.player['position']
    
    no_door_msg = "\033[1;35mNo door to that side of the room, you run into a wall.\033[0m"
    door_locked_msg = "\033[1;35mYou bang on the door but it won't budge. You can't leave the way you came.\033[0m"

    if (y, x) == dungeon_state['entrance_coords']:
        if direction == "w":
            return player_couldnt_move(door_locked_msg)

    if dungeon_state['missing_a_door'][y][x]:
        if direction in dungeon_state['which_doors_missing'][y][x]:
            return player_couldnt_move(no_door_msg)
        
    if direction == "w":
        if y > 0:
            ps.player['position'] = (y - 1, x)
            return True
        else:
            return player_couldnt_move(no_door_msg)
    elif direction == "s":
        if y < len(dungeon_state['dungeon']) - 1:
            ps.player['position'] = (y + 1, x)
            return True
        else:
            return player_couldnt_move(no_door_msg)
    elif direction == "a":
        if x > 0:
            ps.player['position'] = (y, x - 1)
            return True
        else:
            return player_couldnt_move(no_door_msg)
    elif direction == "d":
        if x < len(dungeon_state['dungeon'][0]) - 1:
            ps.player['position'] = (y, x + 1)
            return True
        else:
            return player_couldnt_move(no_door_msg)
        
def player_couldnt_move(message):
    print(message)
    return False


def enter_room(dungeon_state):
    y, x = ps.player['position']
    room = dungeon_state['dungeon'][y][x]
    dungeon_state['visited'][y][x] = True

    room_info = room_data.get(room)
    encounter = room_info.get("encounter")
    description = room_info.get("description")
    item = room_info.get("item")

    if not room_info:
        print("You step into an uncharted room. It's eerily empty.")
        return
    
    # Voi käyttää kauppoja vaikka olis cleared
    if dungeon_state['cleared'][y][x] and room not in dg.SHOP_ROOMS:
        print("\033[1;32mRoom cleared.\033[0m")
        return

    if room != "Dungeon Exit":
        print(f"\033[1;35mYou move into the {room}.\033[0m\n")

    # Ei ylimäärästä linebreakkia filler huoneille
    if room not in dg.FILLER_ROOMS:
        if description:
            print(description + "\n")
    else:
        if description:
            print(description)


    if item:
        add_to_inventory(item)

    dungeon_state['cleared'][y][x] = True
    
    # Laukasee huoneen encounterin
    if encounter:
        handler = ENCOUNTER_HANDLERS.get(encounter)
        if handler:
            return handler()
        else:
            return re.fight_monster(monster_db[encounter])


def add_to_inventory(item):
    if item in ps.player['inventory']:
        ps.player['inventory'][item] += 1
    else:
        ps.player['inventory'][item] = 1


def check_health():
    print(f"Your current health: \033[1;94m{ps.player['health']}\033[0m")
    print(f"Equipped armor: \033[1;36m{ps.player['armor']}\033[0m (remaining protection: \033[1;31m{ps.player['armor_hp']}\033[0m)")
    

def check_inventory():
    print(f"Equipped weapon: \033[1;36m{ps.player['weapon']}\033[0m (Max Hit: \033[1;31m{ps.player['max_hit']}\033[0m)")
    print(f"Gold coins: \033[1;33m{ps.player['gold']}\033[0m")
    print("Your bag:")
    for item, count in ps.player['inventory'].items():
        if count > 1:
            print(f"\033[1;92m{item}\033[0m x{count}")
        else:
            print(f"\033[1;92m{item}\033[0m")
    print(f"\nTotal monster parts: \033[1;32m{sum(ps.player['inventory'].values())}\033[0m")


def show_map(dungeon_state):
    for y, row in enumerate(dungeon_state['dungeon']):
        row_display = []
        for x, room in enumerate(row):
            if (y, x) == ps.player['position']:
                base_cell = f"▶ {room}"
                formatted_cell = f"{base_cell:<18}"
                cell = f"\033[94m{formatted_cell}\033[0m"
            elif dungeon_state['visited'][y][x]:
                if room in dg.SHOP_ROOMS:
                    formatted_cell = f"{room:<18}"
                    cell = f"\033[95m{formatted_cell}\033[0m"
                else:
                    cell = room
            else:
                cell = "???"
            row_display.append(f"{cell:<18}")
        print(" | " + " | ".join(row_display) + " | ")



def game_loop():
    while True:
        dungeon_state = start_game()

        print("\033[1;35mWelcome to the Dungeon of Death, adventurer!\033[0m")
        print("\033[1;36mYou're just outside the entrance looking upon the tall, menacing doors.\033[0m\n")
        while True:
            start_command = input("Press Enter to move into the dungeon if you're brave enough. If not, type 'exit' to leave.\n")

            if start_command == "":
                break
            elif start_command.lower() == "exit":
                return
            
        print("\033[1;35mYou open the door and walk in. The door closes behind you.\033[0m\n")
        show_map(dungeon_state)
        while True:
            command = input("\nEnter command | up(w) / down(s) / right(d) / left(a), health(h) / inventory(i) / map(m), quit |: ").lower()
            replay_or_exit = None

            if command in ["w", "s", "a", "d"]:
                moved = move_player(command, dungeon_state)
                if moved:
                    replay_or_exit = enter_room(dungeon_state)
                
                if replay_or_exit is not None:
                    if replay_or_exit == "replay":
                        break
                    elif replay_or_exit == "exit":
                        return
                
                print()
                show_map(dungeon_state)

            elif command == "m":
                print()
                show_map(dungeon_state)
            elif command == "h":
                check_health()
            elif command == "i":
                check_inventory()
            elif command == "quit":
                print("Goodbye, adventurer.")
                return
            else:
                print("Invalid command")




if __name__ == "__main__":
    # re.set_restart_callback(game_loop)
    game_loop()